from flask import Blueprint, jsonify, request, current_app, send_from_directory
import os
from datetime import datetime
from app import db
from werkzeug.utils import secure_filename
from PIL import Image
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, EtiquetaTipoSitio, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio
from app.classes.validacion import Validacion

crud_sitio_bp = Blueprint('sitio', __name__)

"""
RUTAS DE SITIO:
    CREAR
    MODIFICAR
    ELIMINAR

CONSULTAS ESTAN EN OTRO ARCHIVO
"""