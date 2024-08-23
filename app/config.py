import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pet_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
