from flask import Blueprint, jsonify, redirect, request
#from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario
from app.classes.consulta import Consulta

sitios_bp = Blueprint('consulta sitios', __name__)

@sitios_bp.route('/mostrar_sitios', methods=["GET", "POST"])
def mostrar_sitios():
    
    ## Se obtienen los datos ##
    data = request.get_json()
    cve_tipo_sitio = data.get("cve_tipo_sitio")
    ordenamiento = data.get("ordenamiento")
    pagina = data.get("pagina")
    """
    precio_min = data.get("precio_min")
    precio_max = data.get("precio_max") 
    calificacion_min = data.get("calificacion_min") 
    cve_delegacion = data.get("cve_delegacion")
    
    , precio_min, precio_max, calificacion_min, cve_delegacion
    """
    
    conexion_db = Consulta()
    sitios_encontrados, num_sitios = conexion_db.obtener_sitios(cve_tipo_sitio, ordenamiento, pagina)
    conexion_db.cerrar_conexion_db()
    
    return jsonify(sitios_encontrados, num_sitios), 200

@sitios_bp.route('/mostrar_sitio', methods=["GET"])
def mostrar_info_sitio():
    
    data = request.get_json()
    cve_sitio = data.get("cve_sitio")
    
    conexion_bd = Consulta()
    datos_sitio = conexion_bd.obtener_sitio(cve_sitio)
    conexion_bd.cerrar_conexion_db()
    
    return jsonify(datos_sitio), 200