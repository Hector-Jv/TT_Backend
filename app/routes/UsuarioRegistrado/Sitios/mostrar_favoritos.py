from flask import Blueprint, jsonify
from app import db
from app.models import Sitio, Delegacion, FotoSitio ,Colonia

mostrar_favoritos_bp = Blueprint('mostrar_favoritos', __name__)

@mostrar_favoritos_bp.route('/mostrar_favoritos', methods=["GET"])
def mostrar_favoritos():
    sitios_encontrados = Sitio.query.all() # [sitios]
    
    datos_sitios = []
    for sitio_objeto in sitios_encontrados:
        if sitio_objeto.habilitado == False:
            continue
        
        datos_sitio_dict = {}
        datos_sitio_dict["cve_sitio"] = sitio_objeto.cve_sitio
        datos_sitio_dict["nombre_sitio"] = sitio_objeto.nombre_sitio
        datos_sitio_dict["costo_promedio"] = sitio_objeto.costo_promedio
        datos_sitio_dict["cve_tipo_sitio"] = sitio_objeto.cve_tipo_sitio
        
        arr_imagenes = []
        fotos_encontradas = FotoSitio.query.filter_by(cve_sitio=sitio_objeto.cve_sitio).all()
        if fotos_encontradas:
            for foto_objeto in fotos_encontradas:
                dict_foto = {}
                dict_foto["cve_foto_sitio"] = foto_objeto.cve_foto_sitio
                dict_foto["nombre_imagen"] = foto_objeto.nombre_imagen
                dict_foto["link_imagen"] = foto_objeto.link_imagen
                dict_foto["nombre_autor"] = foto_objeto.nombre_autor
        datos_sitio_dict["imagenes"] = arr_imagenes
        clave_delegacion = Colonia.query.filter_by(cve_colonia=sitio_objeto.cve_colonia).first().cve_delegacion
        datos_sitio_dict["delegacion"] = Delegacion.query.get(clave_delegacion).nombre_delegacion
        datos_sitio_dict["calificacion"] = sitio_objeto.calificacion
        
        datos_sitios.append(datos_sitio_dict)
    
        
    return jsonify(datos_sitios), 200