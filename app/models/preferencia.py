from app import db

class Preferencia(db.Model):
    correo_usuario = db.Column(db.String(100), primary_key=True)
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
