from app import db
from datetime import datetime

class Sitio(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    nombre_sitio = db.Column(db.String(400), nullable=False)
    x_longitud = db.Column(db.Float(precision=10), nullable=False)
    y_latitud = db.Column(db.Float(precision=10), nullable=False)
    direccion = db.Column(db.String(400), nullable=False)
    
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descripcion = db.Column(db.String(400), nullable=True)
    correo_sitio = db.Column(db.String(100), nullable=True)
    fecha_fundacion = db.Column(db.DateTime, nullable=True)
    costo_promedio = db.Column(db.Float(5), nullable=True)
    habilitado = db.Column(db.Boolean, default=True)
    pagina_web = db.Column(db.String(400), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    adscripcion = db.Column(db.String(400), nullable=True)
    
    
    cve_tipo_sitio = db.Column(db.Integer, db.ForeignKey('tipo_sitio.cve_tipo_sitio'), nullable=False)
    cve_colonia = db.Column(db.Integer, db.ForeignKey('colonia.cve_colonia'), nullable=False)
    
    
    tipo_sitio = db.relationship('TipoSitio', backref='sitios')
    colonia = db.relationship('Colonia', backref='sitios')
    