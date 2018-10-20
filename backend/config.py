import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQL_ALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL") or \
            "sqlite:///" + os.path.join(basedir, "dogapp.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
