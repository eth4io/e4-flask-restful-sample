import json
import flask
from flask_pymongo import PyMongo
from flask.ext.sqlalchemy import SQLAlchemy
from requests_oauthlib import OAuth2Session
from credentials.config import Auth, Config, config
from requests.exceptions import HTTPError
from flask.ext.login import LoginManager, login_required, login_user, \
    logout_user, current_user, UserMixin

import google_auth_oauthlib.flow
import google.oauth2.credentials

app = flask.Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(config['dev'])
app.config['SESSION_TYPE'] = 'mongodb'

# app.config["MONGO_DBNAME"] = "e4flask"
# mongo = PyMongo(app, config_prefix='MONGO')





@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login')
def login():
    if current_user.is_authenticated():
        return flask.redirect(flask.url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_BASE_URI, access_type='offline')
    flask.session['oauth_state'] = state
    return flask.render_template('login.html', auth_url=auth_url)


@app.route('/authorize')
def authorize():
    google = OAuth2Session(Auth.CLIENT_ID, scope=Auth.SCOPE, redirect_uri=Auth.REDIRECT_URI)
    authorization_url, state = google.authorization_url(Auth.AUTH_BASE_URI,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline", prompt="select_account")

    # State is used to prevent CSRF, keep this for later.
    flask.session['oauth_state'] = state
    return flask.redirect(authorization_url)


@app.route('/oauth2callback/google', methods=["GET"])
def oauth2callback_google():
    if 'error' in flask.request.args:
        if flask.request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in flask.request.args and 'state' not in flask.request.args:
        return flask.redirect(flask.url_for('login'))
    else:
        google = get_google_auth(state=flask.session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=flask.request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return 'Could not fetch your information.'



def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(Auth.CLIENT_ID, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
    return oauth
