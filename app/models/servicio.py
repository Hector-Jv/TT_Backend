from app import db

class Servicio(db.Model):
    cve_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(100), nullable=False)