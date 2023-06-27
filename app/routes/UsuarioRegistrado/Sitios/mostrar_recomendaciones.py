from flask import Blueprint, jsonify, request
from app import db
from app.models import Historial, Usuario, TipoSitio, Sitio, FotoSitio, Colonia, Delegacion, UsuarioEtiqueta, UsuarioServicio, SitioEtiqueta, ServicioHotel
import json

mostrar_recomendaciones_bp = Blueprint('mostrar_recomendaciones', __name__)

@mostrar_recomendaciones_bp.route('/mostrar_recomendaciones/<string:correo_usuario>', methods=["GET"])
def mostrar_recomendaciones(correo_usuario):
    
    ## VALIDACIONES DE ENTRADA ## 
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
        
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Es necesario ingresar un correo registrado."}), 400


    ## SE HACE EL FILTRADO DE SITIOS ##    
    historiales_usuario = Historial.query.filter_by(correo_usuario = correo_usuario).all()
    cve_sitios_historial_usuario = [historial_usuario.cve_sitio for historial_usuario in historiales_usuario if historial_usuario.visitado]
    
    sitios_encontrados = Sitio.query.all()
    datos_sitios = [] # Contiene la información de todos los sitios en diccionario.
    for sitio in sitios_encontrados:
        if sitio.habilitado == False:
            continue
        datos_sitio_dict = {}
        datos_sitio_dict["cve_sitio"] = sitio.cve_sitio
        datos_sitio_dict["nombre_sitio"] = sitio.nombre_sitio
        datos_sitio_dict["costo_promedio"] = sitio.costo_promedio
        datos_sitio_dict["cve_tipo_sitio"] = sitio.cve_tipo_sitio

        arr_imagenes = []
        fotos_encontradas = FotoSitio.query.filter_by(cve_sitio=sitio.cve_sitio).all() # []
        if fotos_encontradas:
            for foto_objeto in fotos_encontradas:
                dict_foto = {}
                dict_foto["cve_foto_sitio"] = foto_objeto.cve_foto_sitio
                dict_foto["link_imagen"] = foto_objeto.link_imagen
                arr_imagenes.append(dict_foto)
        datos_sitio_dict["imagenes"] = arr_imagenes
        clave_delegacion = Colonia.query.filter_by(cve_colonia=sitio.cve_colonia).first().cve_delegacion
        datos_sitio_dict["delegacion"] = Delegacion.query.get(clave_delegacion).nombre_delegacion
        datos_sitio_dict["calificacion"] = sitio.calificacion
        datos_sitios.append(datos_sitio_dict)
    
    datos_sitios_historial_usuario = [] # Contiene todos los sitios que se encuentren dentro del historial del usuario y que lo haya visitado.
    for datos_sitio in datos_sitios:
        if datos_sitio["cve_sitio"] in cve_sitios_historial_usuario:
            datos_sitios_historial_usuario.append(datos_sitio)
    cve_sitios = [sitio["cve_sitio"]  for sitio in datos_sitios_historial_usuario]
    
    ### SE HACEN LAS RECOMENDACIONES ###
    tipos_sitio = ["museos", "hoteles", "parques", "restaurantes", "teatros", "monumentos"]
    reglas_asociacion = []
    
    for tipo in tipos_sitio:
        with open(f'app/data/reglas_asociacion_{tipo}.json') as f:
            reglas_asociacion = reglas_asociacion + json.load(f)
    
    sitios_recomendados = [] # Sitios que cumplen con alguna regla de asociación.
    for regla in reglas_asociacion:
        cumple = True
        for elemento in regla["antecedente"]:
            if not elemento in cve_sitios:
                cumple = False
                break
        if cumple:
            dict_provisional = {}
            dict_provisional["antecedente"] = regla["antecedente"] 
            dict_provisional["consecuente"] = regla["consecuente"]
            sitios_recomendados.append(dict_provisional)

    cve_sitios_recomendados_sin_repeticiones = set() # Se guardan solo las claves de los sitios recomendados sin repetirse
    for sitio_recomendado in sitios_recomendados:
        for sitio in sitio_recomendado["consecuente"]:
            cve_sitios_recomendados_sin_repeticiones.add(sitio)
    
    datos_sitios_recomendados = [] # Son los datos de los sitios
    for datos_sitio in datos_sitios:
        if datos_sitio["cve_sitio"] in cve_sitios_recomendados_sin_repeticiones:
            datos_sitios_recomendados.append(datos_sitio)
    
    ### ARRANQUE EN FRIO ###
    lista_sitios_en_frio = []
    if not datos_sitios_recomendados:
        print("Dentro de arranque en frio")
        cves_etiquetas = [etiqueta.cve_etiqueta for etiqueta in UsuarioEtiqueta.query.filter_by(correo_usuario = correo_usuario).all()]
        cves_servicios = [servicio.cve_servicio for servicio in UsuarioServicio.query.filter_by(correo_usuario = correo_usuario).all()]
        
        for sitio in datos_sitios:
            if sitio["calificacion"] == None:
                continue
            
            if sitio["calificacion"] > 3:
                lista_sitios_en_frio.append(sitio)
                continue
            
            if sitio["cve_tipo_sitio"] == 1 or sitio["cve_tipo_sitio"] == 6 and len(cves_etiquetas) != 0:
                etiquetas_sitio = [etiquetaSitio.cve_etiqueta for etiquetaSitio in SitioEtiqueta.query.filter_by(cve_sitio=sitio["cve_sitio"]).all()]
                if not etiquetas_sitio:
                    continue
                aux = False
                for etiqueta_sitio in etiquetas_sitio:
                    if etiqueta_sitio in cves_etiquetas:
                        aux = True
                        break
                if aux:
                    lista_sitios_en_frio.append(sitio)
                    continue
            
            if sitio["cve_tipo_sitio"] == 5 and len(cves_servicios) != 0:
                servicios_sitio = [servicioSitio.cve_servicio for servicioSitio in ServicioHotel.query.filter_by(cve_sitio=sitio["cve_sitio"]).all()]
                if not servicios_sitio:
                    continue
                aux = False
                for servicio_sitio in servicios_sitio:
                    if servicio_sitio in cves_servicios:
                        aux = True
                        break
                if aux:
                    lista_sitios_en_frio.append(sitio)
                    continue
        return jsonify(lista_sitios_en_frio), 200
    
    return jsonify(datos_sitios_recomendados), 200

