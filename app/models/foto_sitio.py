from app import db

class FotoSitio(db.Model):
    cve_foto_sitio = db.Column(db.Integer, primary_key=True)
    foto_sitio = db.Column(db.LargeBinary, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    sitio = db.relationship('Sitio', backref='fotos_sitio')