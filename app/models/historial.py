from datetime import datetime
from app import db

class Historial(db.Model):
    cve_historial = db.Column(db.Integer, primary_key=True)
    visitado = db.Column(db.Boolean, default=False)
    fecha_visita = db.Column(db.DateTime, nullable=False)
    correo_usuario = db.Column(db.String(100), db.ForeignKey('usuario.correo_usuario'), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    
    def __init__(self, correo_usuario: int, cve_sitio: int):
        self.visitado = False
        self.fecha_visita = datetime.utcnow()
        self.correo_usuario = correo_usuario
        self.cve_sitio = cve_sitio
        
