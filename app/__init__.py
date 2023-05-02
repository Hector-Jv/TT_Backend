from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.config['JWT_SECRET_KEY'] =  os.environ.get('SECRET_KEY_TOKEN')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    jwt = JWTManager(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    login_manager.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    return app
