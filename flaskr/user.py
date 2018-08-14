from flaskr.alchemy_db_helper import alchemy_db
import datetime


class User(alchemy_db.Model):
    __tablename__ = "users"
    id = alchemy_db.Column(alchemy_db.Integer, unique=True, primary_key=True)
    email = alchemy_db.Column(alchemy_db.String(128), unique=True, nullable=False)
    name = alchemy_db.Column(alchemy_db.String(128), nullable=True)
    avatar_url = alchemy_db.Column(alchemy_db.String(256))
    tokens = alchemy_db.Column(alchemy_db.Text)
    created_at = alchemy_db.Column(alchemy_db.DateTime, default=datetime.datetime.utcnow())