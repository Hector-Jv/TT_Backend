from flask import Blueprint, jsonify, request
from app import db
from app.models import Delegacion, TipoSitio, Etiqueta, Servicio, TipoSitio_Etiqueta
from app.classes.modificar_sitio import modificar_sitio

datos_para_crear_sitio_bp = Blueprint('datos_para_crear_sitio', __name__)

@datos_para_crear_sitio_bp.route('/crear_sitio', methods=['GET'])
def datos_para_crear_sitio():
    datos: dict = {}
    datos["tipo_sitios"] = [tipositio.to_dict() for tipositio in TipoSitio.obtener_tipositios()]
    datos["delegaciones"] = [delegacion.to_dict() for delegacion in Delegacion.obtener_todos_las_delegaciones()]
    datos["servicios"] = [servicio.to_dict() for servicio in Servicio.obtener_todos_los_servicios()]
    datos["etiquetas"] = [etiqueta.to_dict() for etiqueta in Etiqueta.obtener_todas_las_etiquetas()]
    
    return jsonify(datos), 200

@datos_para_crear_sitio_bp.route('/obtener_etiquetas', methods=['GET'])
def obtener_etiquetas():
    etiquetas = [etiqueta.to_dict()["nombre_etiqueta"] for etiqueta in Etiqueta.obtener_todas_las_etiquetas()]
    
    return jsonify({"etiquetas": etiquetas}), 200

