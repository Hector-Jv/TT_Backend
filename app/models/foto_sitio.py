from app import db
from flask import current_app
from .sitio import Sitio
from app.classes.validacion import Validacion

class FotoSitio(db.Model):
    cve_foto_sitio = db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
    link_imagen = db.Column(db.String(400), nullable=False)
    nombre_imagen = db.Column(db.String(400), nullable=True)
    nombre_autor = db.Column(db.String(400), nullable=True)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)

    def __init__(self, link_imagen: str, cve_sitio: int, nombre_autor: str = '', nombre_imagen: str = ''):
        self.link_imagen = link_imagen
        self.cve_sitio = cve_sitio
        self.nombre_imagen = nombre_imagen
        self.nombre_autor = nombre_autor
 