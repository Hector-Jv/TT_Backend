from flask import Blueprint, jsonify, request
from app.system_recomendations.apriori import Apriori
from itertools import groupby
from app.models import Historial, TipoUsuario, Usuario, TipoSitio, Sitio
import json

generar_reglas_bp = Blueprint('Generar reglas asociacion', __name__)

@generar_reglas_bp.route('/generar_reglas', methods=['POST'])
def generar_reglas():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ["correo_usuario", "cve_tipo_sitio", "confianza"]
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400


    correo_usuario = data.get("correo_usuario")
    cve_tipo_sitio = data.get("cve_tipo_sitio")
    confianza = data.get("confianza")
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    if not cve_tipo_sitio or not isinstance(cve_tipo_sitio, int):
        return jsonify({"error": "Es necesario mandar un valor valido en cve_tipo_sitio."}), 400
    
    if not confianza or not isinstance(confianza, int):
        return jsonify({"error": "Es necesario mandar un valor valido en confianza."}), 400
    
    if confianza > 100 or confianza < 20:
        return jsonify({"error": "Se debe ingresar un valor válido en el campo de confianza. (20 a 100)"}), 400
    
    confianza = float(confianza / 100)
    
    ## VALIDACIÓN DE PERMISOS ##
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Es necesario ingresar con un correo registrado."}), 400
        
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    if tipo_usuario.tipo_usuario != 'Administrador':
        return jsonify({"error": "El usuario no es administrador. No puede borrar el sitio."}), 403
    
    ## VALIDACION TIPO DE SITIO ##
    tipositio_encontrado = TipoSitio.query.get(cve_tipo_sitio)
    if not tipositio_encontrado:
        return jsonify({"error": "No existe el tipo sitio ingresado."}), 400
    
    soporte_minimo = 2
    
    historiales_encontrados = Historial.query.all()
    arreglo_historiales = [(historial.correo_usuario, historial.cve_sitio) for historial in historiales_encontrados]
    print(arreglo_historiales)
    arreglo_filtrado = []
    for historial in arreglo_historiales:
        sitio_encontrado: Sitio = Sitio.query.get(historial[1])
        if sitio_encontrado.cve_tipo_sitio == cve_tipo_sitio and sitio_encontrado.habilitado:
            arreglo_filtrado.append(historial)
    
    # Se ordena por correo electronico
    arreglo_filtrado.sort(key=lambda x: x[0])
    
    # Se agrupan por correo electrónico
    historial_usuarios = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(arreglo_filtrado, lambda x: x[0])]
    
    
    sistema_recomendacion = Apriori(historial_usuarios, soporte_minimo, confianza)
    reglas = sistema_recomendacion.iniciar_algoritmo()
    
    with open(f'app/data/reglas_asociacion_{tipositio_encontrado.tipo_sitio}.json', 'w') as f:
        json.dump(reglas, f)
    return jsonify({"mensaje": f"Se han generado las reglas de asociación para los sitios de tipo {tipositio_encontrado.tipo_sitio} con exito."}), 200