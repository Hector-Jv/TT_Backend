from datetime import datetime
from app import db

class Comentario(db.Model):
    cve_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    comentario = db.Column(db.String(400), nullable=False)
    fecha_comentario = db.Column(db.DateTime, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
 
    def __init__(self, comentario: str, cve_historial: int):
        self.comentario = comentario
        self.cve_historial = cve_historial
        self.fecha_comentario = datetime.now()
    