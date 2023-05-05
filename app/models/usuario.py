from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    correo_usuario = db.Column(db.String(100), primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)
    foto_usuario = db.Column(db.LargeBinary, nullable=True)
    cve_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.cve_tipo_usuario'), nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False)

    tipo_usuario = db.relationship('TipoUsuario', backref='usuarios')
    
    def to_dict(self):
        return {
            'correo_usuario': self.correo_usuario,
            'usuario': self.usuario,
            'contrasena': self.contrasena,
            'foto_usuario': self.foto_usuario,
            'cve_tipo_usuario': self.cve_tipo_usuario,
            'habilitado': self.habilitado
        }

