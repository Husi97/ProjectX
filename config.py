# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = 'secret-key-goes-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False