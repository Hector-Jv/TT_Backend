from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.imagen import Imagen
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio
from app.classes.validacion import Validacion

fun_admin_bp = Blueprint('Funciones administrador', __name__)

@fun_admin_bp.route('/sitio', methods=['POST'])
def crear_sitio():
    
    ##  Datos obligatorios ##
    archivo = request.files['imagen']
    
    nombre_sitio = request.form['nombre_sitio']
    x_longitud = request.form['x_longitud']
    y_latitud = request.form['y_latitud']
    direccion = request.form['direccion']
    cve_tipo_sitio = request.form['cve_tipo_sitio']
    cve_delegacion = request.form['cve_delegacion']
    colonia = request.form['colonia']
    
    ## Datos opcionales ##
    
    fecha_actualizacion = request.form['fecha_actualizacion'] # = data.get('', datetime.utcnow()) # datetime
    descripcion = request.form['descripcion']
    correo_sitio = request.form['correo_sitio']
    fecha_fundacion = request.form['fecha_fundacion']
    costo_promedio = request.form['costo_promedio']
    pagina_web = request.form['pagina_web']
    telefono = request.form['telefono']
    adscripcion = request.form['adscripcion']
    horarios = request.form['horarios']
    etiquetas = request.form['etiquetas']
    servicios = request.form['servicios']
    
    ## Validacion de los datos ##
    
    if not Validacion.datos_necesarios(nombre_sitio, x_longitud, y_latitud, direccion, cve_tipo_sitio, cve_delegacion, colonia):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    sitio_encontrado = Sitio.obtener_sitio_por_nombre(nombre_sitio)
    
    if not Validacion.valor_nulo(sitio_encontrado):
        return jsonify({"error": "Ya existe el sitio ingresado."}), 404
    
    colonia_encontrada = Colonia.obtener_colonia_por_nombre(colonia)

    # Se verifica que la colonia exista en la base de datos, sino se crea.
    if Validacion.valor_nulo(colonia_encontrada):
        if not Colonia.agregar_colonia(nombre_colonia=colonia, cve_delegacion=cve_delegacion):
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
        cve_colonia = colonia_encontrada["cve_colonia"]
    ):
        return jsonify({"error": "Hubo un error al querer agregar el sitio."}), 400
    
    sitio_encontrado = Sitio.obtener_sitio_por_nombre(nombre_sitio)
    
    ## Modelos externos a sitio ##
    
    # Horario #
    if not Validacion.valor_nulo(horarios):
        for horario in horarios:
            if not Horario.agregar_horario(
                dia = horario["dia"],
                horario_apertura = horario["horario_apertura"],
                horario_cierre = horario["horario_cierre"],
                cve_sitio = sitio_encontrado["cve_sitio"]
            ):
                return jsonify({"error": "Hubo un error al querer agregar un horario."}), 400
    
    tipo_sitio_encontrado = TipoSitio.obtener_tipositio_por_cve(cve_tipo_sitio)
    
    # Etiqueta #
    if not Validacion.valor_nulo(etiquetas) and tipo_sitio_encontrado["tipo_sitio"] == "Museo" or tipo_sitio_encontrado["tipo_sitio"] == "Restaurante":
        for etiqueta in etiquetas:
            etiqueta_encontrada = Etiqueta.obtener_etiqueta_por_nombre(etiqueta)
            if Validacion.valor_nulo(etiqueta_encontrada):
                Etiqueta.agregar_etiqueta(nombre_etiqueta = etiqueta)
                etiqueta_encontrada = Etiqueta.obtener_etiqueta_por_nombre(etiqueta)

            if not SitioEtiqueta.existe_relacion_etiqueta_y_sitio(
                cve_etiqueta = etiqueta_encontrada["cve_etiqueta"],
                cve_sitio = sitio_encontrado["cve_sitio"]
            ):
                SitioEtiqueta.agregar_relacion(
                    cve_etiqueta = etiqueta_encontrada["cve_etiqueta"],
                    cve_sitio = sitio_encontrado["cve_sitio"]
                )
    
    # Servicio #
    if not Validacion.valor_nulo(servicios) and sitio_encontrado.tipo_sitio == "Hotel":
        for servicio in servicios:
            servicio_encontrado = Servicio.obtener_servicio_por_nombre(nombre_servicio=servicio)
            
            if Validacion.valor_nulo(servicio_encontrado):
                Servicio.agregar_servicio(nombre_servicio = servicio)
                servicio_encontrado = Servicio.obtener_servicio_por_nombre(nombre_servicio=servicio)

            if not ServicioHotel.existe_relacion_servicio_y_hotel(
                cve_sitio = sitio_encontrado["cve_sitio"], 
                cve_servicio=servicio_encontrado["cve_servicio"]
            ):
                ServicioHotel.agregar_relacion(
                    cve_sitio = sitio_encontrado["cve_sitio"],
                    cve_servicio=servicio_encontrado["cve_servicio"]
                )
    
    # Imagen #
    if 'foto' in request.files:
        foto = request.files['foto']
        
        imagen = Imagen(foto)
        
        if not imagen.tamaño_permitido() or not imagen.tamaño_permitido() or not imagen.validar_imagen():
            return jsonify({"error": "Error al guardar la imagen."}), 400
        
        imagen.agregar_imagen('IMG_SITIOS')
            
        FotoSitio.guardar_imagen(imagen.ruta_foto, imagen.nombre_foto, sitio_encontrado["cve_sitio"])
    
    # Si todo sale bien, regresa un json con el nombre de usuario (se va a modificar)
    return jsonify({"mensaje": "Sitio creado con éxito"}), 201
