from app import db

class Historial(db.Model):
    cve_historial = db.Column(db.Integer, primary_key=True)
    favorito = db.Column(db.Boolean, default=False)
    ultima_visita = db.Column(db.DateTime, nullable=False)
    cve_usuario = db.Column(db.String(100), db.ForeignKey('usuario.correo_usuario'), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    usuario = db.relationship('Usuario', backref='historiales')
    sitio = db.relationship('Sitio', backref='historiales')
