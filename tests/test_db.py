import json
from flask import Flask
import unittest
from flaskr.app import db
from flaskr.user import User

class alchemyDbTest(unittest.TestCase):

    # def create_app(self):
        # pass in test configuration

    def setUp(self):
        self.app = Flask(__name__)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        self.app = Flask(__name__)
        db.init_app(self.app)
        # with self.app.app_context():
        #     alchemy_db.drop_all()

    def testUserInsert(self):
        test_user = User(id="101", email='test@email.com', name='full name')
        with self.app.app_context():
            db.session.add(test_user)
            db.session.commit()
            user = User.query.filter_by(id=101).first()
            assert(user, test_user)

    def testUserInsertFromJson(self):
        test_response_json = '{"id": "108344215935035666491", "email": "aikszhang@gmail.com", "verified_email": true, ' \
                             '"name": "Ethan Z (Eth4nZ)", "given_name": "Ethan", "family_name": "Z", ' \
                             '"link": "https://plus.google.com/+EthanZEth4nZ", "picture": ' \
                             '"https://lh4.googleusercontent.com/-DHmm-S5HUSQ/AAAAAAAAAAI/AAAAAAAAHy4/Kqrvxi9jXcM' \
                             '/photo.jpg", "gender": "male", "locale": "en"} '
        user_data = json.loads(test_response_json)
        user_id = user_data['id']
        with self.app.app_context():
            user = User.query.filter_by(id=user_id).first()
        if user is None:
            user = User()
            user.id = user_id
        user.name = user_data['name']
        user.email = user_data['email']
        # user.tokens =
        user.avatar_url = user_data['picture']
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
