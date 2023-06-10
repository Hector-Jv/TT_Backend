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
        "cve_sitio": int(request.form["cve_sitio"])
    }
    
    # Opcionales #
    nombre_sitio = request.form["nombre_sitio"]
    longitud = float(request.form["longitud"])
    latitud = float(request.form["latitud"])
    cve_tipo_sitio = int(request.form["cve_tipo_sitio"]) 
    cve_delegacion = int(request.form["cve_delegacion"])
    colonia = request.form["colonia"]
    
    descripcion = request.form["descripcion"]
    correo = request.form["correo"]
    costo = float(request.form["costo"])
    pagina_web = request.form["pagina_web"]
    telefono = request.form["telefono"]
    adscripcion = request.form["adscripcion"]
    arreglo_etiquetas = request.form["etiquetas"]
    arreglo_servicios = request.form["servicios"]
    
    if arreglo_etiquetas:
        arreglo_etiquetas = json.loads(arreglo_etiquetas)
        
    if arreglo_servicios:
        arreglo_servicios = json.loads(arreglo_servicios)
    
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
    
    if Sitio.query.filter_by(nombre_sitio=nombre_sitio).first():
        return jsonify({"error": "Ya existe un sitio con ese nombre y con la misma dirección."}), 400
    
    obtener_tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
    if not obtener_tipo_sitio:
        return jsonify({"error": "No existe un tipo de sitio registrado con esa clave."}), 400

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
    
    if request.form['nombre_sitio']:
        nombre_sitio = request.form['nombre_sitio']
    if request.form['longitud'] != '':
        longitud = float(request.form['longitud'])
    if request.form['latitud'] != '':
        latitud = float(request.form['latitud'])
    if request.form['cve_tipo_sitio'] != '': 
        cve_tipo_sitio = int(request.form['cve_tipo_sitio'])
    if request.form['cve_delegacion'] != '':
        cve_delegacion = int(request.form['cve_delegacion'])
    if request.form['colonia'] != '':
        colonia = request.form['colonia']
        
    if request.form['descripcion'] != '':
        descripcion = request.form['descripcion']
        
    return jsonify({"mensaje": "Pendiente"}), 200
    if request.form['costo_promedio'] != '':
        costo_promedio = float(request.form['costo_promedio'])
    if request.form['etiquetas'] != '':
        etiquetas = json.loads(request.form['etiquetas'])
    if request.form['servicios'] != '':
        servicios = json.loads(request.form['servicios'])
    
    modificar_sitio(cve_sitio, nombre_sitio, x_longitud, y_latitud, direccion, 
                    cve_tipo_sitio, cve_delegacion, colonia, 
                    descripcion, correo_sitio, costo_promedio, pagina_web, 
                    telefono, adscripcion, horarios, etiquetas, servicios)
    
    return jsonify({"mensaje": "Se han modificado los datos del sitio."}), 201
    