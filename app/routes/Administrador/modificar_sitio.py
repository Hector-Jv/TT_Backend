from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.models import Usuario, TipoUsuario, Sitio, TipoSitio
import json

modificar_sitio_bp = Blueprint('Modificar sitio', __name__)


@modificar_sitio_bp.route('/modificar_sitio', methods=['PUT'])
def ruta_modificar_sitio():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ["correo_usuario", "cve_sitio", 
                       "nombre_sitio", "longitud",
                       "latitud", "cve_tipo_sitio",
                       "cve_delegacion", "colonia",
                       "descripcion", "correo",
                       "costo", "pagina_web",
                       "telefono", "adscripcion",
                       "etiquetas", "servicios"]
    
    for id in identificadores:
        if id not in request.form:
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    obligatorios = {
        "correo_usuario": request.form["correo_usuario"],
        "cve_sitio": request.form["cve_sitio"]
    }
    
    for nombre, valor in obligatorios.items():
        if not valor:
            return jsonify({"error": f"Es necesario mandar un valor valido en {nombre}."}), 400
    
    ## VALIDACION DE PERMISOS ##
    usuario_encontrado: Usuario = Usuario.query.get(obligatorios["correo_usuario"])
    if not usuario_encontrado:
        return jsonify({"error": "Es necesario ingresar con un correo registrado."}), 400
        
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    if tipo_usuario.tipo_usuario != 'Administrador':
        return jsonify({"error": "El usuario no es administrador. No puede borrar el sitio."}), 403
    
    ## VALIDACIONES ADICIONALES ##
    sitio_encontrado: Sitio = Sitio.query.get(obligatorios['cve_sitio'])
    if not sitio_encontrado:
        return jsonify({"error": "El sitio a modificar no existe."}), 404

    ## MODIFICACION DE LOS DATOS ##
    
    ## Datos opcionales ##
    nombre_sitio = None
    longitud = None
    latitud = None
    cve_tipo_sitio = None
    cve_delegacion = None
    colonia = None
    
    descripcion = None
    correo = None
    costo = None
    pagina_web = None
    telefono = None
    adscripcion = None
    arreglo_etiquetas = None 
    arreglo_servicios = None 
    
    # 
    cambio_tipo_sitio = False
    
    if not request.form['nombre_sitio']:
        nombre_sitio = request.form['nombre_sitio']
    if not request.form['longitud']:
        longitud = float(request.form['longitud'])
    if not request.form['latitud']:
        latitud = float(request.form['latitud'])
    if not request.form['cve_tipo_sitio']:
        cambio_tipo_sitio = True
        cve_tipo_sitio = int(request.form['cve_tipo_sitio'])
    if not request.form['cve_delegacion']:
        cve_delegacion = int(request.form['cve_delegacion'])
    if not request.form['colonia']:
        colonia = request.form['colonia']
    
    if not request.form['descripcion']:
        descripcion = request.form['descripcion']
    if not request.form['correo']:
        correo = request.form['correo']
    if not request.form['costo']:
        costo = float(request.form['costo'])
    if not request.form['pagina_web']:
        pagina_web = request.form['pagina_web']
    if not request.form['telefono']:
        telefono = request.form['telefono']
    if not request.form['adscripcion']:
        adscripcion = request.form['adscripcion']
    if not request.form['etiquetas']:
        arreglo_etiquetas = json.loads(request.form['etiquetas'])
    if request.form['servicios']:
        arreglo_servicios = json.loads(request.form['servicios'])
    
    return jsonify({"mensaje": "Todo bien"}), 200
    
    
    return jsonify({"mensaje": "Se han modificado los datos del sitio."}), 201
    