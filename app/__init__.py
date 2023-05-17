from flask import Flask 
from flask_sqlalchemy import SQLAlchemy # Para interacción con base de datos.
from flask_migrate import Migrate # Para hacer migraciones en la base de datos.
from flask_cors import CORS # Para habilitar y configurar el Cross-Origin Resource Sharing (es un mecanismo de seguridad).
from app.config import Config # Para hacer configuraciones.
from flask_login import LoginManager # Para la autenticación y gestión de sesiones. 
from flask_jwt_extended import JWTManager # Para la autenticación y autorización basada en tokens JWT.
import os # Para interactuar con el sistema operativo.
from datetime import timedelta # para representar y manipular intervalos de tiempo.


db = SQLAlchemy() # Instancia para interactuar con la base de datos.
migrate = Migrate() # Intancia para gestionar las migraciones.
login_manager = LoginManager() # Instancia para gestionar la autenticación de usuarios y las sesiones.

def create_app(config_class=Config):
    
    app = Flask(__name__) # Instancia de app Flask.
    app.config.from_object(config_class) # Configura la aplicación utilizando la clase Config importada (ubicado en el archivo config.py).

    app.config['JWT_SECRET_KEY'] =  os.environ.get('SECRET_KEY_TOKEN') # Configura la clave secreta para JWT a partir de una variable de entorno (ubicado en el archivo .env).
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2) # Tiempo de expiración de token de acceso.
    jwt = JWTManager(app) # Instancia JWTManager que se asocia con app.
    
    db.init_app(app) # Inicializa instancia de SQLAlchemy.
    migrate.init_app(app, db) # Inicializa instancia de Migrate
    CORS(app) # Habilita y configura CORS.
    
    login_manager.init_app(app) # Inicializa instancia LoginManager.
    
    app.config["IMG_SITIOS"] = "app/data/sitios"
    app.config["IMG_COMENTARIOS"] = "app/data/comentarios"
    app.config["IMG_PERFIL"] = "app/data/perfil"
    app.config["IMG_INICIO"] = "app/data/inicio"
    

    # Rutas que se han registrado
    from app import routes

    app.register_blueprint(routes.sitio_bp)
    app.register_blueprint(routes.login_bp)
    app.register_blueprint(routes.registro_bp)
    app.register_blueprint(routes.usuario_bp)
    
    return app 
