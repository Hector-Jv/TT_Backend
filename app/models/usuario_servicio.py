from app import db

class UsuarioServicio(db.Model):
    correo_usuario = db.Column(db.String(400), primary_key=True, )
    cve_servicio = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['correo_usuario'],
            ['usuario.correo_usuario'],
        ),
        db.ForeignKeyConstraint(
            ['cve_servicio'],
            ['servicio.cve_servicio'],
        ),
    )
    
    
    def __init__(self, correo_usuario: str, cve_servicio: int):
        self.correo_usuario = correo_usuario
        self.cve_servicio = cve_servicio
    