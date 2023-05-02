from app import db

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
