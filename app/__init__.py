from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from config import Config

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
