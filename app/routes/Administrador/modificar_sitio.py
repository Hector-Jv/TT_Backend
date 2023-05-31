from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.modificar_sitio import modificar_sitio
import json

modificar_sitio_bp = Blueprint('Modificar sitio', __name__)


@modificar_sitio_bp.route('/modificar_sitio', methods=['PUT'])
def ruta_modificar_sitio():
    
    ## Datos obligatorios ##
    if not request.form['cve_sitio']:
        return jsonify({"mensaje": "Hacen falta datos."}), 400
    
    cve_sitio = request.form['cve_sitio']
    
    ## Datos opcionales ##
    nombre_sitio = None
    x_longitud = None
    y_latitud = None
    direccion = None
    cve_tipo_sitio = None
    cve_delegacion = None
    colonia = None
    horarios = None
    etiquetas = None 
    servicios = None 
    fecha_fundacion = None 
    costo_promedio = None
    
    if request.form['nombre_sitio']:
        nombre_sitio = request.form['nombre_sitio']
    if request.form['x_longitud'] != '':
        x_longitud = float(request.form['x_longitud'])
    if request.form['y_latitud'] != '':
        y_latitud = float(request.form['y_latitud'])
    if request.form['direccion'] != '':
        direccion = request.form['direccion']
    if request.form['cve_tipo_sitio'] != '': 
        cve_tipo_sitio = int(request.form['cve_tipo_sitio'])
    if request.form['cve_delegacion'] != '':
        cve_delegacion = int(request.form['cve_delegacion'])
    if request.form['colonia'] != '':
        colonia = request.form['colonia']
    descripcion = request.form['descripcion']
    correo_sitio = request.form['correo_sitio']
    pagina_web = request.form['pagina_web']
    telefono = request.form['telefono']
    adscripcion = request.form['adscripcion']
    
    if request.form['fecha_fundacion'] != '':
        fecha_fundacion = datetime.strptime(request.form['fecha_fundacion'], '%Y-%m-%d')
    if request.form['costo_promedio'] != '':
        costo_promedio = float(request.form['costo_promedio'])
    if request.form['horarios'] != '':
        horarios = json.loads(request.form['horarios'])
    if request.form['etiquetas'] != '':
        etiquetas = json.loads(request.form['etiquetas'])
    if request.form['servicios'] != '':
        servicios = json.loads(request.form['servicios'])
    
    modificar_sitio(cve_sitio, nombre_sitio, x_longitud, y_latitud, direccion, 
                    cve_tipo_sitio, cve_delegacion, colonia, 
                    descripcion, correo_sitio, costo_promedio, pagina_web, 
                    telefono, adscripcion, horarios, etiquetas, servicios)
    
    return jsonify({"mensaje": "Se han modificado los datos del sitio."}), 201
    