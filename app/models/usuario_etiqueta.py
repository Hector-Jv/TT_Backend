from app import db

class UsuarioEtiqueta(db.Model):
    correo_usuario = db.Column(db.String(400), primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['correo_usuario'],
            ['usuario.correo_usuario'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )
    
    
    def __init__(self, correo_usuario: str, cve_etiqueta: int):
        self.correo_usuario = correo_usuario
        self.cve_etiqueta = cve_etiqueta
    