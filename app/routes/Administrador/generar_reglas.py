from flask import Blueprint, jsonify, request
from app.system_recomendations.apriori import Apriori
from itertools import groupby
from app.models import Historial, TipoUsuario, Usuario, Sitio
import json

generar_reglas_bp = Blueprint('generar_reglas', __name__)

@generar_reglas_bp.route('/generar_reglas', methods=['POST'])
def generar_reglas():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ["correo_usuario"]
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400

    correo_usuario = data.get("correo_usuario")
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    ## VALIDACIÓN DE PERMISOS ##
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Es necesario ingresar con un correo registrado."}), 400
        
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    if tipo_usuario.tipo_usuario != 'Administrador':
        return jsonify({"error": "El usuario no es administrador. No puede borrar el sitio."}), 403
    
    
    ### GENERACION DE REGLAS DE ASOCIACION ###
    
    soporte_minimo = 3
    confianza = 1
    
    historiales_encontrados = Historial.query.all()
    arreglo_historiales = [(historial.correo_usuario, historial.cve_sitio) for historial in historiales_encontrados if historial.visitado]
    # print(arreglo_historiales)
    
    
    sitios_filtrados = {
        "museos": [],
        "hoteles": [],
        "parques": [],
        "restaurantes": [],
        "teatros": [],
        "monumentos": []
    }
    for historial in arreglo_historiales:
        sitio_encontrado: Sitio = Sitio.query.get(historial[1])
        if not sitio_encontrado.habilitado:
            continue
        
        if sitio_encontrado.cve_tipo_sitio == 1:
            sitios_filtrados["museos"].append(historial)
        elif sitio_encontrado.cve_tipo_sitio == 5:
            sitios_filtrados["hoteles"].append(historial)
        elif sitio_encontrado.cve_tipo_sitio == 4:
            sitios_filtrados["parques"].append(historial)
        elif sitio_encontrado.cve_tipo_sitio == 6:
            sitios_filtrados["restaurantes"].append(historial)
        elif sitio_encontrado.cve_tipo_sitio == 2:
            sitios_filtrados["teatros"].append(historial)
        elif sitio_encontrado.cve_tipo_sitio == 3:
            sitios_filtrados["monumentos"].append(historial)
            
    
    # Se ordenan
    sitios_filtrados["hoteles"].sort(key=lambda x: x[0])
    sitios_filtrados["museos"].sort(key=lambda x: x[0])
    sitios_filtrados["parques"].sort(key=lambda x: x[0])
    sitios_filtrados["restaurantes"].sort(key=lambda x: x[0])
    sitios_filtrados["teatros"].sort(key=lambda x: x[0])
    sitios_filtrados["monumentos"].sort(key=lambda x: x[0])
    
    # Se agrupan por correo
    agrupacion_sitio = {
        "museos": [],
        "hoteles": [],
        "parques": [],
        "restaurantes": [],
        "teatros": [],
        "monumentos": []
    }
    
    agrupacion_sitio["museos"] = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(sitios_filtrados["museos"], lambda x: x[0])]
    agrupacion_sitio["hoteles"] = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(sitios_filtrados["hoteles"], lambda x: x[0])]
    agrupacion_sitio["parques"] = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(sitios_filtrados["parques"], lambda x: x[0])]
    agrupacion_sitio["restaurantes"] = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(sitios_filtrados["restaurantes"], lambda x: x[0])]
    agrupacion_sitio["teatros"] = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(sitios_filtrados["teatros"], lambda x: x[0])]
    agrupacion_sitio["monumentos"] = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(sitios_filtrados["monumentos"], lambda x: x[0])]
    
    sistemas_recomendacion = {
        "museos": Apriori(agrupacion_sitio["museos"], soporte_minimo, confianza),
        "hoteles": Apriori(agrupacion_sitio["hoteles"], soporte_minimo, confianza),
        "parques": Apriori(agrupacion_sitio["parques"], soporte_minimo, confianza),
        "restaurantes": Apriori(agrupacion_sitio["restaurantes"], soporte_minimo, confianza),
        "teatros": Apriori(agrupacion_sitio["teatros"], soporte_minimo, confianza),
        "monumentos": Apriori(agrupacion_sitio["monumentos"], soporte_minimo, confianza),
    }
    
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_recomendacion = {executor.submit(recomendacion.iniciar_algoritmo): recomendacion for recomendacion in sistemas_recomendacion.values()}
        # print("Variable future: ", future_to_recomendacion)
        for future in concurrent.futures.as_completed(future_to_recomendacion):
            tipo_sitio = list(sistemas_recomendacion.keys())[list(sistemas_recomendacion.values()).index(future_to_recomendacion[future])]
            reglas = future.result()
            with open(f'app/data/reglas_asociacion_{tipo_sitio}.json', 'w') as f:
                json.dump(reglas, f)
    
    """
    reglas_museos = sistemas_recomendacion["museos"].iniciar_algoritmo()
    print(f"Número de reglas de museos: {len(reglas_museos)} ")
    reglas_hoteles = sistemas_recomendacion["hoteles"].iniciar_algoritmo()
    print(f"Número de reglas de hoteles: {len(reglas_hoteles)} ")
    reglas_parques = sistemas_recomendacion["parques"].iniciar_algoritmo()
    print(f"Número de reglas de parques: {len(reglas_parques)} ")
    reglas_restaurantes = sistemas_recomendacion["restaurantes"].iniciar_algoritmo()
    print(f"Número de reglas de restaurantes: {len(reglas_restaurantes)} ")
    reglas_teatros = sistemas_recomendacion["teatros"].iniciar_algoritmo()
    print(f"Número de reglas de teatros: {len(reglas_teatros)} ")
    reglas_monumentos = sistemas_recomendacion["monumentos"].iniciar_algoritmo()
    print(f"Número de reglas de monumentos: {len(reglas_monumentos)} ")
    
    
    with open(f'app/data/reglas_asociacion_museos.json', 'w') as f:
        json.dump(reglas_museos, f)
    with open(f'app/data/reglas_asociacion_hoteles.json', 'w') as f:
        json.dump(reglas_hoteles, f)
    with open(f'app/data/reglas_asociacion_parques.json', 'w') as f:
        json.dump(reglas_parques, f)
    with open(f'app/data/reglas_asociacion_restaurantes.json', 'w') as f:
        json.dump(reglas_restaurantes, f)
    with open(f'app/data/reglas_asociacion_teatros.json', 'w') as f:
        json.dump(reglas_teatros, f)
    with open(f'app/data/reglas_asociacion_monumentos.json', 'w') as f:
        json.dump(reglas_monumentos, f)
    """
    return jsonify({"mensaje": f"Se han generado las reglas de asociación con exito."}), 200