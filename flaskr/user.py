from flaskr.alchemy_db_helper import alchemy_db
import datetime


class User(alchemy_db.Model):
    __tablename__ = "users"
    id = alchemy_db.Column(alchemy_db.Text, unique=True, primary_key=True)
    email = alchemy_db.Column(alchemy_db.String(128), unique=True, nullable=False)
    name = alchemy_db.Column(alchemy_db.String(128), nullable=True)
    avatar_url = alchemy_db.Column(alchemy_db.String(256))
    tokens = alchemy_db.Column(alchemy_db.Text)
    active = alchemy_db.Column(alchemy_db.Boolean, default=True)
    created_at = alchemy_db.Column(alchemy_db.DateTime, default=datetime.datetime.utcnow())

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

