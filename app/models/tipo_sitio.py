from app import db

class TipoSitio(db.Model):
    cve_tipo_sitio = db.Column(db.Integer, primary_key=True)
    tipo_sitio = db.Column(db.String(100), nullable=False)
    