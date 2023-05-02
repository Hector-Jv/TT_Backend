from app import db

class TipoUsuario(db.Model):
    cve_tipo_usuario = db.Column(db.Integer, primary_key=True)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    