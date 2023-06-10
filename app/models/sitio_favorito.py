from app import db

class SitioFavorito(db.Model):
    correo_usuario = db.Column(db.String(100), primary_key=True)
    cve_sitio = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['correo_usuario'],
            ['usuario.correo_usuario'],
        ),
    )
    
    
    def __init__(self, cve_sitio: int, correo_usuario: str):
        self.correo_usuario = correo_usuario
        self.cve_sitio = cve_sitio
    