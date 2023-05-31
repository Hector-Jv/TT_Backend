from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.imagen import Imagen
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio, Historial, Calificacion, CalificacionHotel, CalificacionRestaurante, Comentario, FotoComentario
from app.classes.validacion import Validacion
from app.classes.modificar_sitio import modificar_sitio
import json

datos_para_crear_sitio_bp = Blueprint('datos_para_crear_sitio', __name__)

@datos_para_crear_sitio_bp.route('/crear_sitio', methods=['GET'])
def datos_para_crear_sitio():
    datos: dict = {}
    datos["tipo_sitios"] = [tipositio.to_dict() for tipositio in TipoSitio.obtener_tipositios()]
    datos["delegaciones"] = [delegacion.to_dict() for delegacion in Delegacion.obtener_todos_las_delegaciones()]
    datos["servicios"] = [servicio.to_dict() for servicio in Servicio.obtener_todos_los_servicios()]
    datos["etiquetas"] = [etiqueta.to_dict() for etiqueta in Etiqueta.obtener_todas_las_etiquetas()]
    
    return jsonify(datos), 200