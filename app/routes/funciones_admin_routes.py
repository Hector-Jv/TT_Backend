from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.imagen import Imagen
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio
from app.classes.validacion import Validacion
import json

fun_admin_bp = Blueprint('Funciones administrador', __name__)

@fun_admin_bp.route('/crear_sitio', methods=['GET'])
def datos_para_crear_sitio():
    datos: dict = {}
    datos["tipo_sitios"] = [tipositio.to_dict() for tipositio in TipoSitio.obtener_tipositios()]
    datos["delegaciones"] = [delegacion.to_dict() for delegacion in Delegacion.obtener_todos_las_delegaciones()]
    datos["servicios"] = [servicio.to_dict() for servicio in Servicio.obtener_todos_los_servicios()]
    datos["etiquetas"] = [etiqueta.to_dict() for etiqueta in Etiqueta.obtener_todas_las_etiquetas()]
    
    return jsonify(datos), 200

@fun_admin_bp.route('/crear_sitio', methods=['POST'])
def crear_sitio():
    
    ##  Datos obligatorios ##
    if not Validacion.datos_necesarios(request.form['nombre_sitio'], request.form['x_longitud'], request.form['y_latitud'], request.form['direccion'], request.form['cve_tipo_sitio'], request.form['cve_delegacion'], request.form['colonia']):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    nombre_sitio = request.form['nombre_sitio']
    x_longitud = float(request.form['x_longitud'])
    y_latitud = float(request.form['y_latitud'])
    direccion = request.form['direccion']
    cve_tipo_sitio = int(request.form['cve_tipo_sitio'])
    cve_delegacion = int(request.form['cve_delegacion'])
    colonia = request.form['colonia']
    
    ## Datos opcionales ##
    
    descripcion = request.form['descripcion']
    correo_sitio = request.form['correo_sitio']
    pagina_web = request.form['pagina_web']
    telefono = request.form['telefono']
    adscripcion = request.form['adscripcion']
    horarios = None
    etiquetas = None 
    servicios = None 
    fecha_fundacion = None 
    costo_promedio = None
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
    
    ## Validacion de los datos ##
    
    sitio_encontrado = Sitio.obtener_sitio_por_nombre(nombre_sitio)
    
    if not Validacion.valor_nulo(sitio_encontrado):
        return jsonify({"error": "Ya existe el sitio ingresado."}), 404
    
    colonia_encontrada = Colonia.obtener_colonia_por_nombre(colonia)

    # Se verifica que la colonia exista en la base de datos, sino se crea.
    if Validacion.valor_nulo(colonia_encontrada):
        if not Colonia.agregar_colonia(colonia, cve_delegacion):
            return jsonify({"error": "Hubo un error al querer agregar la colonia."}), 400
        colonia_encontrada = Colonia.obtener_colonia_por_nombre(colonia)
    
    if not Sitio.agregar_sitio(
        nombre_sitio=nombre_sitio, 
        x_longitud=x_longitud, 
        y_latitud=y_latitud,
        direccion=direccion,
        descripcion=descripcion, 
        correo_sitio=correo_sitio,
        fecha_fundacion=fecha_fundacion, 
        costo_promedio=costo_promedio,
        pagina_web=pagina_web, 
        telefono=telefono, 
        adscripcion=adscripcion,
        cve_tipo_sitio = cve_tipo_sitio,
        cve_colonia = colonia_encontrada.cve_colonia
    ):
        return jsonify({"error": "Hubo un error al querer agregar el sitio."}), 400
    
    sitio_encontrado: Sitio = Sitio.obtener_sitio_por_nombre(nombre_sitio)
    
    ## Modelos externos a sitio ##
    
    # Horario #
    if not Validacion.valor_nulo(horarios):
        for horario in horarios:
            if not Horario.agregar_horario(
                dia = horario["dia"],
                horario_apertura = horario["horario_apertura"],
                horario_cierre = horario["horario_cierre"],
                cve_sitio = sitio_encontrado.cve_sitio
            ):
                return jsonify({"error": "Hubo un error al querer agregar un horario."}), 400
    
    tipo_sitio_encontrado: TipoSitio = TipoSitio.obtener_tipositio_por_cve(cve_tipo_sitio)
    
    # Etiqueta #
    if not Validacion.valor_nulo(etiquetas) and tipo_sitio_encontrado.tipo_sitio == "Museo" or tipo_sitio_encontrado.tipo_sitio == "Restaurante":
        for cve_etiqueta in etiquetas:
            etiqueta_encontrada = Etiqueta.obtener_etiqueta_por_cve(cve_etiqueta)
            if Validacion.valor_nulo(etiqueta_encontrada):
                return jsonify({"error": "No existe la etiqueta indicada."}), 400

            SitioEtiqueta.agregar_relacion(
                cve_etiqueta = cve_etiqueta,
                cve_sitio = sitio_encontrado.cve_sitio
            )
    
    # Servicio #
    if not Validacion.valor_nulo(servicios) and sitio_encontrado.tipo_sitio == "Hotel":
        for cve_servicio in servicios:
            servicio_encontrado = Servicio.obtener_servicio_por_cve(cve_servicio)
            
            if Validacion.valor_nulo(servicio_encontrado):
                return jsonify({"error": "No existe el servicio indicado."}), 400

            ServicioHotel.agregar_relacion(
                cve_sitio = sitio_encontrado.cve_sitio,
                cve_servicio=servicio_encontrado.cve_servicio
            )
    
    ## Manejo de imagen ##
    print("E")
    if 'foto_sitio' in request.files:
        archivo = request.files['foto_sitio']
        
        if archivo.filename != '':
            
            if not Imagen.verificar_extension(archivo):
                return jsonify({"error": "La imagen no tiene una extensión válida. "}), 400
            
            if not Imagen.tamaño_permitido(archivo):
                return jsonify({"error": "La imagen es demasiado grande. "}), 400
            
            if not Imagen.validar_imagen(archivo):
                return jsonify({"error": "Hubo un problema al intentar abrir la imagen. "}), 400
            
            nombre_imagen = Imagen.guardar(foto=archivo, nombre=nombre_sitio, ruta="IMG_SITIOS")

            if not FotoSitio.guardar_imagen(nombre_imagen, sitio_encontrado.cve_sitio):
                return jsonify({"error": "Hubo un problema al intentar guardar la imagen. "}), 400
    
    return jsonify({"mensaje": "Sitio creado con éxito"}), 201

@fun_admin_bp.route('/eliminar_sitio', methods=['DELETE'])
def eliminar_sitio():
    
    """
    data = request.get_json()
    
    cve_sitio = data.get(cve_sitio)
    """

@fun_admin_bp.route('/modificar_sitio', methods=['PUT'])
def modificar_sitio():
    pass
