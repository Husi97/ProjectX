# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Cv(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=False, nullable=True)
    lastname = db.Column(db.String(80), unique=False, nullable=True)
    birthday = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(256), nullable=True)
    job = db.Column(db.String(256), nullable=True)
    education = db.Column(db.String(256), nullable=True)
    summery = db.Column(db.String(256), nullable=True)

