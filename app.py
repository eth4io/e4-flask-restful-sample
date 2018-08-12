import os
import json
from flask import Flask, session, request, jsonify, render_template
from flask_pymongo import PyMongo
from requests_oauthlib import OAuth2Session
from credentials.config import Auth, Config, config
from werkzeug.serving import make_ssl_devcert

app = Flask(__name__)
app.config.from_object(config['dev'])
app.config['SESSION_TYPE'] = 'mongodb'

# app.config["MONGO_DBNAME"] = "e4flask"
# mongo = PyMongo(app, config_prefix='MONGO')



@app.route('/')
def hello_world():
    return 'Hello World!'


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(Auth.CLIENT_ID, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
    return oauth


@app.route('/login')
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)


@app.route('/callback')
def callback():
    google = get_google_auth(state=session['oauth_state'])
    resp = google.get(Auth.USER_INFO)
    if resp.status_code == 200:
        user_data = resp.json()
        email = user_data['email']
        print("Success: ", email)


if __name__ == '__main__':
    make_ssl_devcert('./ssl', host='localhost')
    app.run(debug = True, ssl_context = ('./ssl.crt', './ssl.key'))
