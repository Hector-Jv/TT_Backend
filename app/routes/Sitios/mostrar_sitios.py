from flask import Blueprint, jsonify
from app import db
from app.models import Sitio, Delegacion, FotoSitio ,Colonia, SitioEtiqueta, ServicioHotel, Etiqueta, Servicio

mostrar_sitios_bp = Blueprint('mostrar_sitios', __name__)

@mostrar_sitios_bp.route('/mostrar_sitios', methods=["GET"])
def mostrar_sitios():
    sitios_encontrados = Sitio.query.all() # [sitios]
    
    datos_sitios = []
    for sitio_objeto in sitios_encontrados:
        if sitio_objeto.habilitado == False:
            continue
        
        datos_sitio_dict = {
            "etiquetas": [],
            "servicios": []
        }
        datos_sitio_dict["cve_sitio"] = sitio_objeto.cve_sitio
        datos_sitio_dict["nombre_sitio"] = sitio_objeto.nombre_sitio
        datos_sitio_dict["costo_promedio"] = sitio_objeto.costo_promedio
        datos_sitio_dict["cve_tipo_sitio"] = sitio_objeto.cve_tipo_sitio
        datos_sitio_dict["habilitado"] = sitio_objeto.habilitado
        
        arr_imagenes = []
        fotos_encontradas = FotoSitio.query.filter_by(cve_sitio=sitio_objeto.cve_sitio).all() # []
        if fotos_encontradas:
            for foto_objeto in fotos_encontradas:
                dict_foto = {}
                dict_foto["cve_foto_sitio"] = foto_objeto.cve_foto_sitio
                dict_foto["link_imagen"] = foto_objeto.link_imagen
                arr_imagenes.append(dict_foto)
        datos_sitio_dict["imagenes"] = arr_imagenes
        clave_delegacion = Colonia.query.filter_by(cve_colonia=sitio_objeto.cve_colonia).first().cve_delegacion
        datos_sitio_dict["delegacion"] = Delegacion.query.get(clave_delegacion).nombre_delegacion
        datos_sitio_dict["calificacion"] = sitio_objeto.calificacion
        
        etiquetas_de_sitio = SitioEtiqueta.query.filter_by(cve_sitio=sitio_objeto.cve_sitio).all()
        if etiquetas_de_sitio:
            for etiqueta in etiquetas_de_sitio:
                etiqueta_dict = {}
                etiqueta_encontrada: Etiqueta = Etiqueta.query.get(etiqueta.cve_etiqueta)
                etiqueta_dict["value"] = etiqueta_encontrada.cve_etiqueta
                etiqueta_dict["label"] = etiqueta_encontrada.nombre_etiqueta
                datos_sitio_dict["etiquetas"].append(etiqueta_dict)
        
        servicios_de_sitio = ServicioHotel.query.filter_by(cve_sitio=sitio_objeto.cve_sitio).all()
        if servicios_de_sitio:
            for servicio in servicios_de_sitio:
                servicio_dict = {}
                servicio_encontrado: Servicio = Servicio.query.get(servicio.cve_servicio)
                servicio_dict["value"] = servicio_encontrado.cve_servicio
                servicio_dict["label"] = servicio_encontrado.nombre_servicio
                datos_sitio_dict["etiquetas"].append(servicio_dict)
        
        
        datos_sitios.append(datos_sitio_dict)
    
        
    return jsonify(datos_sitios), 200
