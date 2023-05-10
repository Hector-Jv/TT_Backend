from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from werkzeug.utils import secure_filename
from PIL import Image
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, EtiquetaTipoSitio, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio
from app.utils.validaciones import datos_necesarios

sitio_bp = Blueprint('sitio', __name__)

@sitio_bp.route('/imagen', methods=['POST'])
def obtener_imagenes():
    imagenes = request.files.getlist('imagenes')
    cve_sitio = request.form.get('cve_sitio')

    for imagen in imagenes:
        es_valida, mensaje_error = FotoSitio.validar_imagen(imagen)
        if not es_valida:
            return jsonify({"error": mensaje_error}), 400

        FotoSitio.guardar_imagen(imagen, 10)

    return jsonify({"message": "Se añadió correctamente"}), 201



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
    
    # Datos recibidos del administrador.
    data = request.get_json()

    # Se extraen los datos recibidos.
    # Son obligatorios.
    nombre_sitio = data.get('nombre_sitio')
    x_longitud = data.get('x_longitud')
    y_latitud = data.get('y_latitud')
    direccion = data.get('direccion')
    
    # Llave foraneas
    tipo_sitio = data.get('tipo_sitio')
    delegacion = data.get('delegacion')
    colonia = data.get('colonia')
    
    # Pueden ser nulos.
    fecha_actualizacion = data.get('fecha_actualizacion', datetime.utcnow()) 
    descripcion = data.get('descripcion')
    correo_sitio = data.get('correo_sitio')
    fecha_fundacion = data.get('fecha_fundacion')
    costo_promedio = data.get('costo_promedio')
    pagina_web = data.get('pagina_web')
    telefono = data.get('telefono')
    adscripcion = data.get('adscripcion')
    
    # Son opcionales y pertenecen a otros modelos.
    horarios = data.get('horarios') # Debe ser una tupla o lista con todos los horarios.
    etiquetas = data.get('etiquetas')
    servicios = data.get('servicios')
    
    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(nombre_sitio, x_longitud, y_latitud, direccion, tipo_sitio, delegacion, colonia):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    # Busca si el nombre del sitio ingresado se encuentra registrado.
    existe_sitio = Sitio.query.filter_by(nombre_sitio=nombre_sitio).first()
    
    # Se verifica que no haya un sitio registrado en la base de datos.
    if existe_sitio is not None:
        return jsonify({"error": "Ya existe el sitio ingresado."}), 404
    
    # Busca el tipo de sitio que pertenece.
    tipo_sitio_objeto = TipoSitio.query.filter_by(tipo_sitio=tipo_sitio).first()
    
    # Busca la delegacion al que pertenece.
    delegacion_objeto = Delegacion.query.filter_by(nombre_delegacion=delegacion).first()
    
    # Busca la colonia al que pertenece.
    colonia_objeto = Colonia.query.filter_by(nombre_colonia=colonia).first()
    
    # Se verifica que la colonia exista en la base de datos, sino se crea.
    if colonia_objeto is None:
        nueva_colonia = Colonia(
            nombre_colonia = colonia,
            cve_delegacion = delegacion_objeto.cve_delegacion
        )
        # Se añade la colonia a la sesión.
        db.session.add(nueva_colonia)
        # Se confirma y se aplican los cambios realizados en la base de datos.
        db.session.commit()
    
        # Busca la colonia al que pertenece.
        colonia_objeto = Colonia.query.filter_by(nombre_colonia=colonia).first()
    
    # Se crea el objeto Sitio
    sitio = Sitio(
        nombre_sitio=nombre_sitio, 
        x_longitud=x_longitud, 
        y_latitud=y_latitud,
        direccion=direccion,
        
        fecha_actualizacion=fecha_actualizacion,
        descripcion=descripcion, 
        correo_sitio=correo_sitio,
        fecha_fundacion=fecha_fundacion, 
        costo_promedio=costo_promedio,
        pagina_web=pagina_web, 
        telefono=telefono, 
        adscripcion=adscripcion,
        
        cve_tipo_sitio = tipo_sitio_objeto.cve_tipo_sitio,
        cve_colonia = colonia_objeto.cve_colonia
    )
    # Se añade la colonia a la sesión.
    db.session.add(sitio)
    # Se confirma y se aplican los cambios realizados en la base de datos.
    db.session.commit()
    
    # Buscamos el sitio recien ingresado.
    sitio_objeto = Sitio.query.filter_by(nombre_sitio=nombre_sitio).first()
    
    # Si se especificaron los horarios del sitio de interes.
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
    
    # Si se especificaron las etiquetas del sitio de interés y pertenece a grupo adecuado.
    if etiquetas is not None and tipo_sitio == "Museo" or tipo_sitio == "Restaurante":
        for etiqueta in etiquetas:
            # Verifica que se encuentre registrada la etiqueta en la base de datos.
            etiqueta_objeto = Etiqueta.query.filter_by(nombre_etiqueta=etiqueta).first()
            # Si la etiqueta no esta registrada en la base de datos, se agrega.
            if etiqueta_objeto is None:
                nueva_etiqueta = Etiqueta(
                    nombre_etiqueta = etiqueta
                )
                # Se añade la etiqueta a la sesión.
                db.session.add(nueva_etiqueta)
                # Se confirma y se aplican los cambios realizados en la base de datos.
                db.session.commit()
                # Se obtiene la etiqueta recien agregada a la base de datos.
                etiqueta_objeto = Etiqueta.query.filter_by(nombre_etiqueta=etiqueta).first()
            
            # Verifica que se no este registrada la relación entre sitio y etiqueta en la base de datos.
            relacion_objeto_SE = SitioEtiqueta.query.filter_by(cve_sitio=sitio_objeto.cve_sitio, cve_etiqueta=etiqueta_objeto.cve_etiqueta).first()
            
            if relacion_objeto_SE is None:
                # Se crea la relación entre sitio y etiqueta.
                nueva_relacion = SitioEtiqueta(
                    cve_sitio = sitio_objeto.cve_sitio,
                    cve_etiqueta = etiqueta_objeto.cve_etiqueta
                )
                
                # Se añade la relación entre sitio y etiqueta a la sesión.
                db.session.add(nueva_relacion)
                # Se confirma y se aplican los cambios realizados en la base de datos.
                db.session.commit() 
            
            # Verifica que se no este registrada la relación entre tipo sitio y etiqueta en la base de datos.
            relacion_objeto_TSE = EtiquetaTipoSitio.query.filter_by(cve_tipo_sitio=sitio_objeto.cve_tipo_sitio, cve_etiqueta=etiqueta_objeto.cve_etiqueta).first()
            
            if relacion_objeto_TSE is None:
                # Se crea la relación entre tipo sitio y etiqueta.
                nueva_relacion = EtiquetaTipoSitio(
                    cve_tipo_sitio=sitio_objeto.cve_tipo_sitio,
                    cve_etiqueta=etiqueta_objeto.cve_etiqueta
                )
                
                # Se añade la relación entre tipo sitio y etiqueta a la sesión.
                db.session.add(nueva_relacion)
                # Se confirma y se aplican los cambios realizados en la base de datos.
                db.session.commit() 
            
    # Si se especificaron las etiquetas del sitio de interés y pertenece a grupo adecuado.
    if servicios is not None and tipo_sitio == "Hotel":
        for servicio in servicios:
            # Verifica que se encuentre registrada el servicio en la base de datos.
            servicio_objeto = Servicio.query.filter_by(nombre_servicio=servicio).first()
            # Si la etiqueta no esta registrada en la base de datos, se agrega.
            if servicio_objeto is None:
                nuevo_servicio = Servicio(
                nombre_servicio = servicio
                )
                # Se añade el servicio a la sesión.
                db.session.add(nuevo_servicio)
                # Se confirma y se aplican los cambios realizados en la base de datos.
                db.session.commit()
                # Se obtiene el servicio recien agregado a la base de datos.
                servicio_objeto = Servicio.query.filter_by(nombre_servicio=servicio).first()

            # Verifica que se no este registrada la relación entre sitio y servicio en la base de datos.
            relacion_objeto_SS = ServicioHotel.query.filter_by(cve_sitio = sitio_objeto.cve_sitio, cve_servicio=servicio_objeto.cve_servicio).first()
            
            if relacion_objeto_SS is None:
                # Se crea la relación entre sitio y servicio.
                nueva_relacion = ServicioHotel(
                    cve_sitio = sitio_objeto.cve_sitio,
                    cve_servicio=servicio_objeto.cve_servicio
                )
                
                # Se añade la relación entre sitio y servicio a la sesión.
                db.session.add(nueva_relacion)
                # Se confirma y se aplican los cambios realizados en la base de datos.
                db.session.commit() 
            
    # Faltan las imagenes de los sitios de interés.
    
    # Si todo sale bien, regresa un json con el nombre de usuario (se va a modificar)
    return jsonify({"message": "Sitio creado con éxito"}), 201

@sitio_bp.route('/sitio', methods=['DELETE'])
def eliminar_sitio():
    
    # Datos recibidos del administrador.
    data = request.get_json()
    
    # Se extraen los datos recibidos.
    identificador_sitio = data.get('cve_sitio')
    
    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(identificador_sitio):
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
    """
    Actualiza los valores de un sitio en la base de datos.

    Recibe un JSON en la solicitud con los datos a actualizar.
    
    Parámetros:
        "cve_sitio": 10, # Entero
        "nombre_sitio": "", # String
        "x_longitud": -99.15177, # Float
        "y_latitud": 19.4729, # Float
        "direccion": "", # String 
        "cve_tipo_sitio": 3, # Entero
        "cve_delegacion": 2, # Entero
        "colonia": "Liberación", # String
        "fecha_actualizacion": "", # DateTime
        "descripcion": null, # String
        "correo_sitio": "", # String
        "fecha_fundacion": "", #DateTime
        "costo_promedio": null, # Float
        "pagina_web": "", # String
        "telefono": "", # String 
        "adscripcion": null, # String
        "horarios": [
            {
                "dia": "", # String
                "horario_apertura": "", # Time 07:30:00
                "horario_cierre": "" # Time 22:00:00
            }
        ],
        # En caso de que sea Museo o Restaurante.
        "Etiquetas": [
            "", # String 
        ],
        # En caso de que sea Hotel
        "servicios": [
            "", #String
        ]
    
    Los campos que no se incluyan en el JSON se mantendrán 
    sin cambios en la base de datos.

    Devuelve un JSON con un mensaje de éxito si la operación fue 
    exitosa, o un JSON con un mensaje de error si algo fue mal.
    """
    
    ### Se obtienen todos los datos del usuario ###
    
    # Datos recibidos del administrador.
    data = request.get_json()

    # Es obligatorio
    cve_sitio = data['cve_sitio']
    
    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(cve_sitio):
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
    
    