from flaskr.alchemy_db_helper import db
import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Text, unique=True, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=True)
    avatar_url = db.Column(db.String(256))
    tokens = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.email

    # for Flask-Login
    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

