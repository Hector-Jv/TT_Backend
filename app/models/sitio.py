from app import db
from datetime import datetime

class Sitio(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    ## OBLIGATORIO ##
    nombre_sitio = db.Column(db.String(400), nullable=False, unique=True)
    longitud = db.Column(db.Float(precision=10), nullable=False)
    latitud = db.Column(db.Float(precision=10), nullable=False)
    cve_tipo_sitio = db.Column(db.Integer, db.ForeignKey('tipo_sitio.cve_tipo_sitio'), nullable=False)
    cve_colonia = db.Column(db.Integer, db.ForeignKey('colonia.cve_colonia'), nullable=False)
    
    ## OPCIONALES ##
    descripcion = db.Column(db.String(800), nullable=True)
    correo_sitio = db.Column(db.String(100), nullable=True)
    costo_promedio = db.Column(db.Float(5), nullable=True)
    pagina_web = db.Column(db.String(400), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    adscripcion = db.Column(db.String(400), nullable=True) 
    calificacion = db.Column(db.Float(5), nullable=True)
    
    ## DATOS GENERADOS ##
    num_calificaciones = db.Column(db.Integer, nullable=True, default=0)
    habilitado = db.Column(db.Boolean, default=True)
    
    def __init__(self, nombre_sitio: str, longitud: float, latitud: float, cve_tipo_sitio: int, cve_colonia: int,
                 descripcion: str = "", correo_sitio: str = "", costo_promedio: float = 0, 
                 pagina_web: str = "", telefono: str = "", adscripcion: str = "", calificacion: float = None):
        
        # Obligatorios #
        self.nombre_sitio = nombre_sitio
        self.longitud = longitud
        self.latitud = latitud
        self.cve_tipo_sitio = cve_tipo_sitio
        self.cve_colonia = cve_colonia
        # Opcionales #
        self.descripcion = descripcion
        self.correo_sitio = correo_sitio
        self.costo_promedio = costo_promedio
        self.pagina_web = pagina_web
        self.telefono = telefono
        self.adscripcion = adscripcion
        self.calificacion = calificacion
        # Datos generados #
        self.num_calificaciones = 0
        self.habilitado = True
    