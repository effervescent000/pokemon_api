from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app, supports_credentials=True)

    with app.app_context():
        from .models import User, Note

        db.create_all()