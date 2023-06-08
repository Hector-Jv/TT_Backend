from app import db
from app.classes.validacion import Validacion

class ServicioHotel(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_servicio = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_servicio'],
            ['servicio.cve_servicio'],
        ),
    )
    
    def __init__(self, cve_sitio: int, cve_servicio: int):
        self.cve_sitio = cve_sitio
        self.cve_servicio = cve_servicio