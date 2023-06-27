from datetime import datetime
from app import db

class Comentario(db.Model):
    cve_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    comentario = db.Column(db.String(400), nullable=True)
    calificacion = db.Column(db.Float(5), nullable=True)
    fecha_comentario = db.Column(db.DateTime, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
 
    def __init__(self, cve_historial: int, calificacion: int, comentario: str= ""):
        self.comentario = comentario
        self.cve_historial = cve_historial
        self.calificacion = calificacion
        self.fecha_comentario = datetime.now()
    