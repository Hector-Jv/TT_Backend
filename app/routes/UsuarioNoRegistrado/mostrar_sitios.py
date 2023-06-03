from flask import Blueprint, jsonify, request
from app import db
from app.classes.consulta import Consulta
from app.models import Sitio, TipoSitio, Delegacion, Colonia, Historial, Calificacion

mostrar_sitios_unr_bp = Blueprint('mostrar_sitios_unr', __name__)

"""
@mostrar_sitios_unr_bp.route('/mostrar_sitios', methods=["GET", "POST"])
def mostrar_sitios():
    
    ## Se obtienen los datos ##
    data = request.get_json()
    
    # Datos por defecto
    cve_tipo_sitio = 1
    ordenamiento = 1
    pagina = 0
    precio_min = 0
    precio_max = 99999
    calificacion_min = 0
    cve_delegacion = 1
    
    if data.get("cve_tipo_sitio"):
        cve_tipo_sitio = data.get("cve_tipo_sitio")
    if data.get("ordenamiento"):
        ordenamiento = data.get("ordenamiento")
    if data.get("pagina"):
        pagina = data.get("pagina")
    if data.get("precio_min"):
        precio_min = data.get("precio_min")
    if data.get("precio_max") :
        precio_max = data.get("precio_max")
    if data.get("calificacion_min"):
        calificacion_min = data.get("calificacion_min")
    if data.get("cve_delegacion"):
        cve_delegacion = data.get("cve_delegacion")

    ## Obtener sitios de la base de datos ##    
    
    sitios = []
    
    try:
        conexion_db = Consulta()
        conexion_db.cursor.callproc('obtener_sitios', 
                                    [cve_tipo_sitio, ordenamiento, 
                                     pagina, precio_min,
                                     precio_max, calificacion_min,
                                     cve_delegacion])
        resultados = conexion_db.cursor.stored_results()
            
        for resultado in resultados:
            for sitio in resultado.fetchall():
                print(sitio)
    
    finally:
        conexion_db.cerrar_conexion_db()
    
    
    
    return jsonify({"mensaje": "Ve en consola"}), 200
"""

@mostrar_sitios_unr_bp.route('/mostrar_sitios', methods=["GET", "POST"])
def mostrar_sitios():

    ## Se obtienen los datos ##
    data = request.get_json()
    
    # Datos por defecto
    cve_tipo_sitio = 1
    ordenamiento = 1
    pagina = 0
    precio_min = 0
    precio_max = 99999
    calificacion_min = 0
    cve_delegacion = 1
    
    if data.get("cve_tipo_sitio"):
        cve_tipo_sitio = data.get("cve_tipo_sitio")
    if data.get("ordenamiento"):
        ordenamiento = data.get("ordenamiento")
    if data.get("pagina"):
        pagina = data.get("pagina")
    if data.get("precio_min"):
        precio_min = data.get("precio_min")
    if data.get("precio_max") :
        precio_max = data.get("precio_max")
    if data.get("calificacion_min"):
        calificacion_min = data.get("calificacion_min")
    if data.get("cve_delegacion"):
        cve_delegacion = data.get("cve_delegacion")
    
    import time
    start_time = time.time()
    
    for colonia, sitio in db.session.query(Colonia, Sitio).join(Sitio).join(Delegacion):
        print(colonia.cve_colonia, sitio.cve_colonia, sitio.cve_sitio)
        
    
        
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("El tiempo de ejecución fue: ", elapsed_time, " segundos")
        
    return jsonify({"mensaje": "Ve la consola"}), 200