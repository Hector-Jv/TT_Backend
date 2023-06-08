from flask import Flask
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
import cloudinary
import cloudinary.uploader


db = SQLAlchemy() # Instancia para interactuar con la base de datos.
migrate = Migrate() # Intancia para gestionar las migraciones.
login_manager = LoginManager()


def create_app(config_class=Config):
    
    app = Flask(__name__) # Instancia de app Flask.
    app.config.from_object(config_class) # Configura la aplicación utilizando la clase Config importada (ubicado en el archivo config.py).

    app.config['JWT_SECRET_KEY'] =  os.environ.get('SECRET_KEY_TOKEN') # Configura la clave secreta para JWT a partir de una variable de entorno (ubicado en el archivo .env).
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2) # Tiempo de expiración de token de acceso.
    jwt = JWTManager(app) # Instancia JWTManager que se asocia con app.
    
    db.init_app(app) # Inicializa instancia de SQLAlchemy.
    migrate.init_app(app, db) # Inicializa instancia de Migrate
    CORS(app) # Habilita y configura CORS.
    
    cloudinary.config(
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),  
        api_key = os.environ.get('CLOUDINARY_API_KEY'),  
        api_secret = os.environ.get('CLOUDINARY_API_SECRET'), 
        secure = True
    )
    login_manager.init_app(app)

    # Rutas que se han registrado
    from .routes.Administrador import all_blueprints as administrador_blueprints
    from .routes.Autenticacion import all_blueprints as autenticacion_blueprints
    from .routes.Sitios import all_blueprints as sitios_blueprints
    from .routes.UsuarioRegistrado import all_blueprints as usuario_registrado_blueprints
    
    for bp in autenticacion_blueprints:
        app.register_blueprint(bp)
        
    for bp in sitios_blueprints:
        app.register_blueprint(bp)
    
    for bp in administrador_blueprints:
        app.register_blueprint(bp)
    
    for bp in usuario_registrado_blueprints:
        app.register_blueprint(bp)
    
    return app 
