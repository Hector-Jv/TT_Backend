from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  UserMixin

class Usuario(db.Model, UserMixin):
    correo_usuario = db.Column(db.String(100), primary_key=True, unique=True)
    usuario = db.Column(db.String(100), nullable=False, unique=True)
    contrasena_hash  = db.Column(db.String(128))
    link_imagen = db.Column(db.String(200), nullable=True)
    cve_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.cve_tipo_usuario'), nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, correo_usuario: str, usuario: str, contrasena: str, link_imagen: str = None):
        self.correo_usuario = correo_usuario
        self.usuario = usuario
        self.contrasena = contrasena
        self.link_imagen = link_imagen
        self.cve_tipo_usuario = 1
        self.habilitado = True
    
    def verificar_contrasena(self, contrasena: str):
        return check_password_hash(self.contrasena_hash, contrasena)
            
    @property
    def contrasena(self): 
        raise AttributeError('La contraseña no es un atributo legible')

    @contrasena.setter
    def contrasena(self, contrasena: str):
        self.contrasena_hash = generate_password_hash(contrasena)
