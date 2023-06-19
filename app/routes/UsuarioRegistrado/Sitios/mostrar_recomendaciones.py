from flask import Blueprint, jsonify, request
from app import db
from app.models import Historial, Usuario, TipoSitio, Sitio, FotoSitio, Colonia, Delegacion
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

    sitios_encontrados = Sitio.query.all() # [sitios]
    
    datos_sitios = []
    for sitio_objeto in sitios_encontrados:
        if sitio_objeto.habilitado == False:
            continue
        
        historial_encontrado: Historial = Historial.query.filter_by(cve_sitio=sitio_objeto.cve_sitio, correo_usuario=correo_usuario).first()
        if not historial_encontrado:
            continue
        
        if not historial_encontrado.visitado:
            continue
        
        datos_sitio_dict = {}
        datos_sitio_dict["cve_historial"] = historial_encontrado.cve_historial
        datos_sitio_dict["cve_sitio"] = sitio_objeto.cve_sitio
        datos_sitio_dict["nombre_sitio"] = sitio_objeto.nombre_sitio
        datos_sitio_dict["costo_promedio"] = sitio_objeto.costo_promedio
        datos_sitio_dict["cve_tipo_sitio"] = sitio_objeto.cve_tipo_sitio
        
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
        print("cve_sitio obtenido: ", datos_sitio_dict["cve_sitio"])
        datos_sitios.append(datos_sitio_dict)
    
    cve_sitios = [sitio["cve_sitio"]  for sitio in datos_sitios]
    
    ### RECOMENDACIONES DE MUSEOS ###
    tipos_sitio = ["museos", "hoteles", "parques", "restaurantes", "teatros", "monumentos"]
    reglas_asociacion = []
    
    for tipo in tipos_sitio:
        with open(f'app/data/reglas_asociacion_{tipo}.json') as f:
            reglas_asociacion = reglas_asociacion + json.load(f)
    
    sitios_recomendados = []
    for regla in reglas_asociacion:
        print(regla)
        cumple = True
        for elemento in regla["antecedente"]:
            if not elemento in cve_sitios:
                cumple = False
                break
        if cumple:
            print(regla)
            dict_provisional = {}
            dict_provisional["antecedente"] = regla["antecedente"] 
            dict_provisional["consecuente"] = regla["consecuente"]
            dict_provisional["cve_tipo_sitio"] = 1
            sitios_recomendados.append(dict_provisional)

    
    cve_sitios_recomendados_sin_repeticiones = set()    
    for sitio_recomendado in sitios_recomendados:
        for sitio in sitio_recomendado["consecuente"]:
            cve_sitios_recomendados_sin_repeticiones.add(sitio)
          
    
    lista_sitios_recomendados = []
    for sitio in datos_sitios:
        if sitio["cve_sitio"] in cve_sitios_recomendados_sin_repeticiones:
            lista_sitios_recomendados.append(sitio)
    
    
    return jsonify(lista_sitios_recomendados), 200

