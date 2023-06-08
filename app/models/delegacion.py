from app import db

class Delegacion(db.Model):
    cve_delegacion = db.Column(db.Integer, primary_key=True)
    nombre_delegacion = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre_delegacion: str):
        self.nombre_delegacion = nombre_delegacion
