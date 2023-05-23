from flask import Blueprint, jsonify, request, current_app, send_from_directory
import os
from datetime import datetime
from app import db
from werkzeug.utils import secure_filename
from PIL import Image
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio
from app.classes.validacion import Validacion

sitio_bp = Blueprint('sitio', __name__)

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
    
    