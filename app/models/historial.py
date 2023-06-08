from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from .usuario import Usuario
from .sitio import Sitio
from app.classes.validacion import Validacion

class Historial(db.Model):
    cve_historial = db.Column(db.Integer, primary_key=True)
    me_gusta = db.Column(db.Boolean, default=False)
    fecha_visita = db.Column(db.DateTime, nullable=False)
    correo_usuario = db.Column(db.String(100), db.ForeignKey('usuario.correo_usuario'), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    
    def __init__(self, correo_usuario: int, cve_sitio: int):
        self.me_gusta = False
        self.fecha_visita = datetime.utcnow()
        self.correo_usuario = correo_usuario
        self.cve_sitio = cve_sitio
        
