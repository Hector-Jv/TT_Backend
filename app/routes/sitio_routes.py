from flask import Blueprint, jsonify, request, current_app, send_from_directory
import os
from datetime import datetime
from app import db
from werkzeug.utils import secure_filename
from PIL import Image
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio
from app.classes.validacion import Validacion

sitio_bp = Blueprint('sitio', __name__)

@sitio_bp.route('/sitios', methods=['GET'])
def obtener_sitios():
    
    # Se obtienen todos los sitios registrados.
    sitios = Sitio.query.all()
    
    lista_sitios = []
    
    for sitio in sitios:
        info_sitio = {}
        info_sitio["cve_sitio"] = sitio.cve_sitio
        info_sitio["nombre_sitio"] = sitio.nombre_sitio
        info_sitio["x_longitud"] = sitio.x_longitud
        info_sitio["y_latitud"] = sitio.y_latitud
        info_sitio["direccion"] = sitio.direccion
        info_sitio["fecha_actualizacion"] = sitio.fecha_actualizacion
        info_sitio["descripcion"] = sitio.descripcion
        info_sitio["correo_sitio"] = sitio.correo_sitio
        info_sitio["fecha_fundacion"] = sitio.fecha_fundacion
        info_sitio["costo_promedio"] = sitio.costo_promedio
        info_sitio["habilitado"] = sitio.habilitado
        info_sitio["pagina_web"] = sitio.pagina_web
        info_sitio["telefono"] = sitio.telefono
        info_sitio["adscripcion"] = sitio.adscripcion
        
        # Busca el tipo de sitio que pertenece.
        tipo_sitio_objeto = TipoSitio.query.filter_by(cve_tipo_sitio=sitio.cve_tipo_sitio).first()
        
        info_sitio["tipo_sitio"] = tipo_sitio_objeto.tipo_sitio
        info_sitio["habilitado"] = sitio.habilitado
        
        # Busca la colonia al que pertenece.
        colonia_objeto = Colonia.query.filter_by(cve_colonia=sitio.cve_colonia).first()
        
        # Busca la delegacion al que pertenece.
        delegacion_objeto = Delegacion.query.filter_by(cve_delegacion=colonia_objeto.cve_delegacion).first()
        
        info_sitio["colonia"] = colonia_objeto.nombre_colonia
        info_sitio["delegacion"] = delegacion_objeto.nombre_delegacion
        
        # Faltan las fotografías, horarios, etiquetas, servicios
        lista_sitios.append(info_sitio)
        
    return jsonify(lista_sitios), 200

@sitio_bp.route('/sitio', methods=['POST'])
def crear_sitio():
    
    ##  Datos obligatorios ##
    
    data = request.get_json()
    nombre_sitio = data.get('nombre_sitio') # str
    x_longitud = data.get('x_longitud') # float
    y_latitud = data.get('y_latitud') # float
    direccion = data.get('direccion') # str
    cve_tipo_sitio = data.get('cve_tipo_sitio') # int
    cve_delegacion = data.get('cve_delegacion') #int
    colonia = data.get('colonia') # str
    
    ## Datos opcionales ##
    
    fecha_actualizacion = data.get('fecha_actualizacion', datetime.utcnow()) # datetime
    descripcion = data.get('descripcion') # str
    correo_sitio = data.get('correo_sitio') # str
    fecha_fundacion = data.get('fecha_fundacion') # datetime
    costo_promedio = data.get('costo_promedio') # float
    pagina_web = data.get('pagina_web') # str
    telefono = data.get('telefono') # str
    adscripcion = data.get('adscripcion') # str
    horarios = data.get('horarios') # list
    etiquetas = data.get('etiquetas') # list
    servicios = data.get('servicios') # list
    
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
            
    # Faltan las imagenes de los sitios de interés.
    
    # Si todo sale bien, regresa un json con el nombre de usuario (se va a modificar)
    return jsonify({"mensaje": "Sitio creado con éxito"}), 201

@sitio_bp.route('/sitio', methods=['DELETE'])
def eliminar_sitio():
    
    # Datos recibidos del administrador.
    data = request.get_json()
    
    # Se extraen los datos recibidos.
    identificador_sitio = data.get('cve_sitio')
    
    # Se verifica que hayan entregado los datos necesarios.
    if not Validacion.datos_necesarios(identificador_sitio):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    # Busca si el identificador del sitio ingresado se encuentra registrado en la base de datos.
    existe_sitio = Sitio.query.filter_by(cve_sitio=identificador_sitio).first()
    
    # Se verifica que no haya un sitio registrado en la base de datos.
    if existe_sitio is None:
        return jsonify({"error": "No existe el sitio a eliminar."}), 404
    
    ################ ELIMINACIÓN DE RELACIONES #####################
    
    ### FotoSitio ###
    
    # Se busca si hay fotos del sitio almacenadas en la base de datos.
    fotos_de_sitio = FotoSitio.query.filter(FotoSitio.cve_sitio == identificador_sitio).all()
    
    # Se verifica que haya una relación con el modelo fotositio en la base de datos.
    if fotos_de_sitio is not None:
        for foto_de_sitio in fotos_de_sitio:
            # Se especifica la imagen de sitio a eliminar.
            db.session.delete(foto_de_sitio)
            # Se confirman los cambios.
            db.session.commit()
    
    ### Horario ###
    
    # Se busca si hay horarios del sitio almacenadas en la base de datos.
    horarios_de_sitio = Horario.query.filter(Horario.cve_sitio == identificador_sitio).all()
    
    # Se verifica que haya horarios relacionados con el sitio en la base de datos.
    if horarios_de_sitio is not None:
        for horario_de_sitio in horarios_de_sitio:
            # Se especifica el horario del sitio a eliminar.
            db.session.delete(horario_de_sitio)
            # Se confirman los cambios.
            db.session.commit()
    
    ### SitioEtiqueta ###
    
    # Se busca si tiene relaciones con alguna etiqueta almacenada en la base de datos.
    etiquetas_de_sitio = SitioEtiqueta.query.filter(SitioEtiqueta.cve_sitio == identificador_sitio).all()
    
    print(type(etiquetas_de_sitio))
    print(etiquetas_de_sitio)
    
    # Se verifica que haya etiquetas relacionadas con el sitio en la base de datos.
    if etiquetas_de_sitio is not None:
        for etiqueta_de_sitio in etiquetas_de_sitio:
            # Se especifica la relación del sitio a eliminar.
            db.session.delete(etiqueta_de_sitio)
            # Se confirman los cambios.
            db.session.commit()
            
    ### ServicioHotel ###
    
    # Se busca si tiene relaciones con algún servicio almacenada en la base de datos.
    servicios_de_sitio = ServicioHotel.query.filter(ServicioHotel.cve_sitio == identificador_sitio).all()

    # Se verifica que haya servicios relacionados con el sitio en la base de datos.
    if servicios_de_sitio is not None:
        for servicio_de_sitio in servicios_de_sitio:
            # Se especifica la relación del sitio a eliminar.
            db.session.delete(servicio_de_sitio)
            # Se confirman los cambios.
            db.session.commit()
            
    ### Se elimina el sitio ###
    
    # Se especifica el sitio a eliminar.
    db.session.delete(existe_sitio)
    # Se confirman los cambios.
    db.session.commit()

    # Si todo sale bien, regresa un mensaje de que el sitio a sido eliminado.
    return jsonify({"message": "Sitio eliminado."}), 201

@sitio_bp.route('/sitio', methods=['PUT'])
def modificar_sitio():
    
    # Datos obligatorios
    data = request.get_json()
    cve_sitio = data['cve_sitio']
    
    # Se verifica que hayan entregado los datos necesarios.
    if not Validacion.datos_necesarios(cve_sitio):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    # Busca si el nombre del sitio ingresado se encuentra registrado.
    sitio = Sitio.query.get(cve_sitio)
    
    # Se verifica que exista el sitio en la base de datos.
    if sitio is None:
        return jsonify({"error": "No existe el sitio ha modificar."}), 404
    
    # get acepta dos argumentos: la clave del valor ha obtener y un valor predeterminado.
    sitio.nombre_sitio = data.get('nombre_sitio', sitio.nombre_sitio)
    sitio.x_longitud = data.get('x_longitud', sitio.x_longitud)
    sitio.y_latitud = data.get('y_latitud', sitio.y_latitud)
    sitio.direccion = data.get('direccion', sitio.direccion)
    sitio.fecha_actualizacion = data.get('fecha_actualizacion', datetime.utcnow())
    sitio.descripcion = data.get('descripcion', sitio.descripcion)
    sitio.correo_sitio = data.get('correo_sitio', sitio.correo_sitio)
    sitio.fecha_fundacion = data.get('fecha_fundacion', sitio.fecha_fundacion)
    sitio.costo_promedio = data.get('costo_promedio', sitio.costo_promedio)
    sitio.pagina_web = data.get('pagina_web', sitio.pagina_web)
    sitio.telefono = data.get('telefono', sitio.telefono)
    sitio.adscripcion = data.get('adscripcion', sitio.adscripcion)
    
    # Actualizar tipo sitio
    tipo_sitio_bd = TipoSitio.query.get(data.get('cve_tipo_sitio'))
    sitio.cve_tipo_sitio = data.get(tipo_sitio_bd.cve_tipo_sitio, sitio.cve_tipo_sitio)
    
    # Actualizar delegación y colonia
    delegacion = Delegacion.query.get(data.get('cve_delegacion'))
    colonia = Colonia.query.get(sitio.cve_colonia)
    
    registros_colonia = Colonia.query.filter_by(nombre_colonia=colonia.nombre_colonia).all()
    if len(registros_colonia) == 1:
        colonia.nombre_colonia = data.get('colonia', colonia.nombre_colonia)
        colonia.cve_delegacion = data.get(delegacion.cve_delegacion, colonia.cve_delegacion)
    else:
        nueva_colonia = Colonia(
            nombre_colonia = data.get('colonia'),
            cve_delegacion = delegacion.cve_delegacion
        )
        # Se añade la colonia a la sesión.
        db.session.add(nueva_colonia)
        db.session.commit()
        colonia = Colonia.query.get(nueva_colonia.cve_colonia)
    
    sitio.cve_colonia = data.get(colonia.cve_colonia, sitio.cve_colonia)    
    
    # Actualizar horarios
    if data.get('horarios') is not None:
        lista_horarios = Horario.query.filter_by(cve_sitio=cve_sitio).all()
        print(lista_horarios)
        
        
    """
    if horarios is not None:
        for horario in horarios:
            horario_nuevo = Horario(
                dia = horario["dia"],
                horario_apertura = horario["horario_apertura"],
                horario_cierre = horario["horario_cierre"],
                cve_sitio = sitio_objeto.cve_sitio
            )
            # Se añade el horario a la sesión.
            db.session.add(horario_nuevo)
            # Se confirma y se aplican los cambios realizados en la base de datos.
            db.session.commit()
    if 
    
    # Son opcionales y pertenecen a otros modelos.
    horarios = data.get('horarios') # Debe ser una tupla o lista con todos los horarios.
    etiquetas = data.get('etiquetas')
    servicios = data.get('servicios')
    """
    db.session.commit()

    return jsonify({"mensaje": "Actualizacion completada"}), 200
    
    