from flask import Flask 
from flask_sqlalchemy import SQLAlchemy # Para interacción con base de datos.
from flask_migrate import Migrate # Para hacer migraciones en la base de datos.
from flask_cors import CORS # Para habilitar y configurar el Cross-Origin Resource Sharing (es un mecanismo de seguridad).
from app.config import Config # Para hacer configuraciones.
from flask_jwt_extended import JWTManager # Para la autenticación y autorización basada en tokens JWT.
import os # Para interactuar con el sistema operativo.
from datetime import timedelta # para representar y manipular intervalos de tiempo.
import cloudinary
import cloudinary.uploader


db = SQLAlchemy() # Instancia para interactuar con la base de datos.
migrate = Migrate() # Intancia para gestionar las migraciones.

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
