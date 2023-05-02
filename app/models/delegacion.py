from app import db

class Delegacion(db.Model):
    cve_delegacion = db.Column(db.Integer, primary_key=True)
    nombre_delegacion = db.Column(db.String(100), nullable=False)
    
    