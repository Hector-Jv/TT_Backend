from app import db

class Etiqueta(db.Model):
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    nombre_etiqueta = db.Column(db.String(100), nullable=False)