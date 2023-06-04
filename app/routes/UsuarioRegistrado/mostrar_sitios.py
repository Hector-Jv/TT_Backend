from flask import Blueprint, jsonify, request
from app import db
from app.classes.consulta import Consulta
from app.models import Sitio, TipoSitio, Delegacion, FotoSitio ,Colonia, Historial, Calificacion

mostrar_sitios_bp = Blueprint('mostrar_sitios_ur', __name__)

@mostrar_sitios_bp.route('/mostrar_sitios', methods=["GET"])
def mostrar_sitios():
    sitios_encontrados = Sitio.query.all() # [sitios]
    
    datos_sitios = []
    for sitio_objeto in sitios_encontrados:
        datos_sitio_dict = {}
        datos_sitio_dict["nombre_sitio"] = sitio_objeto.nombre_sitio
        datos_sitio_dict["costo_promedio"] = sitio_objeto.costo_promedio
        datos_sitio_dict["cve_tipo_sitio"] = sitio_objeto.cve_tipo_sitio
        datos_sitio_dict["imagenes"] = [foto_objeto.nombre_imagen for foto_objeto in FotoSitio.query.filter_by(cve_sitio=sitio_objeto.cve_sitio).all()]
        clave_delegacion = Colonia.query.filter_by(cve_colonia=sitio_objeto.cve_colonia).first().cve_delegacion
        datos_sitio_dict["delegacion"] = Delegacion.query.get(clave_delegacion).nombre_delegacion
        
        # datos_sitio_dict["calificacion"] = 
        
        datos_sitios.append(datos_sitio_dict)
    
        
    return jsonify(datos_sitios), 200
