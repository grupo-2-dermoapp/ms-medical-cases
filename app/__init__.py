from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("dermoapp-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings_module)
    if not app.config.get('TESTING', False):
        app.config.from_pyfile('production.py', silent=True)
    else:
        app.config.from_pyfile('stage.py', silent=True)

    db.init_app(app)
    # migrate.init_app(app, db, render_as_batch=True)
    with app.app_context():
        db.create_all()

    return app