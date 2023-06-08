from app import db

class Colonia(db.Model):
    cve_colonia = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_colonia = db.Column(db.String(200), nullable=False)
    cve_delegacion = db.Column(db.Integer, db.ForeignKey('delegacion.cve_delegacion'), nullable=False)
    
    def __init__ (self, nombre_colonia: str, cve_delegacion: int):
        self.nombre_colonia = nombre_colonia
        self.cve_delegacion = cve_delegacion
    