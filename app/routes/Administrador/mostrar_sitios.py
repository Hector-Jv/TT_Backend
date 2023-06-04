from flask import Blueprint, jsonify, request

from app.classes.consulta import Consulta

mostrar_sitios_admin_bp = Blueprint('Mostrar sitios administrador', __name__)

@mostrar_sitios_admin_bp.route('/mostrar_sitios', methods=["POST"])
def mostrar_sitios_admin():
    
    ## Se obtienen los datos ##
    data = request.get_json()
    cve_tipo_sitio = data.get("cve_tipo_sitio", 1)
    ordenamiento = data.get("ordenamiento", 1)
    pagina = data.get("pagina", 0)
    
    conexion_db = Consulta()
    sitios_encontrados = conexion_db.obtener_sitios(cve_tipo_sitio, ordenamiento, pagina)
    conexion_db.cerrar_conexion_db()
    
    return jsonify(sitios_encontrados), 200