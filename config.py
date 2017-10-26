import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
HOST = '0.0.0.0'
