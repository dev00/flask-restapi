from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import db, get_data, models
db.create_all()
