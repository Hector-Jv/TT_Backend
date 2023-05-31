from flask import Blueprint, jsonify, request

from app.classes.consulta import Consulta

mostrar_sitios_admin_bp = Blueprint('Mostrar sitios administrador', __name__)

@mostrar_sitios_admin_bp.route('/mostrar_sitios_admin', methods=["GET", "POST"])
def mostrar_sitios_admin():
    
    ## Se obtienen los datos ##
    data = request.get_json()
    cve_tipo_sitio = data.get("cve_tipo_sitio", 1)
    ordenamiento = data.get("ordenamiento", 1)
    pagina = data.get("pagina", 0)
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