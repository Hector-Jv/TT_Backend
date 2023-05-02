from app import db

class SitioEtiqueta(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )
