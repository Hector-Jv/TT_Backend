from app import db
from datetime import datetime

class Horario(db.Model):
    cve_horario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    dia = db.Column(db.String(100), nullable=False)
    horario_apertura = db.Column(db.Time, nullable=False)
    horario_cierre = db.Column(db.Time, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    def __init__(self, dia: str, horario_apertura: str, horario_cierre: str, cve_sitio: int):
        self.dia = dia
        self.horario_apertura = datetime.strptime(horario_apertura, "%H:%M").time()
        self.horario_cierre = datetime.strptime(horario_cierre, "%H:%M").time()
        self.cve_sitio = cve_sitio
        