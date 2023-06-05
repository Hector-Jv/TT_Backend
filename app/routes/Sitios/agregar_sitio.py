import json
from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.imagen import Imagen
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio, Historial, Calificacion, CalificacionHotel, CalificacionRestaurante, Comentario, FotoComentario
from app.classes.validacion import Validacion
from app.classes.modificar_sitio import modificar_sitio
import cloudinary.uploader

agregar_sitio_bp = Blueprint('agregar_sitio', __name__)

@agregar_sitio_bp.route('/crear_sitio', methods=['POST'])
def crear_sitio(): 
    
    # Datos ingresados #
    try:
        # Modelo Sitio
        nombre_sitio = request.form["nombre_sitio"]
        longitud = request.form["longitud"]
        latitud = request.form["latitud"]
        descripcion = request.form["descripcion"]
        correo = request.form["correo"]
        costo = request.form["costo"]
        pagina_web = request.form["pagina_web"]
        telefono = request.form["telefono"]
        adscripcion = request.form["adscripcion"]
        arr_tipo_sitio = request.form["tipo_sitio"] # arreglo diccionarios 
        
        # Modelo Colonia y Delegacion #   
        arr_delegacion = request.form["delegacion"] # arreglo de diccionarios
        colonia = request.form["colonia"]
        
        # Modelo SitioEtiqueta #
        arr_etiquetas = request.form["etiquetas"] # arreglo diccionarios
        
        # Modelo Horario
        arr_horario = request.form["horarios"] # arreglo de diccionarios
        
    except Exception as e:
        return jsonify({"error": "Hubo un error al recibir los datos."}), 400
        
    # Conversiones #
    longitud = float(longitud)
    latitud = float(latitud)
    costo = float(costo) if costo else 0
    
    arr_tipo_sitio = json.loads(arr_tipo_sitio)
    cve_tipo_sitio = int(arr_tipo_sitio[0]["value"])
    
    arr_etiquetas = json.loads(arr_etiquetas)
    arreglo_etiquetas = []
    for etiqueta in arr_etiquetas:
        arreglo_etiquetas.append(etiqueta["value"])
    arr_etiquetas = arreglo_etiquetas
    
    arr_delegacion = json.loads(arr_delegacion)
    cve_delegacion = int(arr_delegacion[0]["value"])
    
    
    # Validaciones #
    if Sitio.query.filter_by(nombre_sitio=nombre_sitio, x_longitud=longitud, y_latitud=latitud).first():
        return jsonify({"error": "Ya existe un sitio con ese nombre y con la misma dirección."}), 400
    
    calificacion_sitio = {
        "promedio": 0
    }
    
    obtener_tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
    
    if obtener_tipo_sitio.tipo_sitio == "Hotel":
        calificacion_sitio["calificaciones_especificas"] = {
            "limpieza": 0,
            "atencion": 0,
            "instalaciones": 0
        }
    if obtener_tipo_sitio.tipo_sitio == "Restaurante":
        calificacion_sitio["calificaciones_especificas"] = {
            "limpieza": 0,
            "atencion": 0,
            "costo": 0,
            "sabor": 0
        }    
    
    obtener_colonia = Colonia.query.filter_by(nombre_colonia=colonia).first()
    
    try:
        # Insertar colonia
        if not obtener_colonia:
            crear_colonia = Colonia(
                colonia, 
                cve_delegacion
            )
            db.session.add(crear_colonia)
            obtener_colonia = crear_colonia

        # Insertar sitio
        nuevo_sitio = Sitio(
            # Obligatorios #
            nombre_sitio, 
            longitud, 
            latitud,
            cve_tipo_sitio,
            obtener_colonia.cve_colonia,
            # Opcionales #
            descripcion,
            correo,
            costo,
            pagina_web,
            telefono,
            adscripcion,
            calificacion_sitio
        )
        db.session.add(nuevo_sitio)
        db.session.flush()

        # Insertar horarios
        for horario in arr_horario:
            nuevo_horario = Horario(
                horario["dia"],
                horario["horario_apertura"],
                horario["horario_cierre"],
                horario["cve_sitio"]
            )
            db.session.add(nuevo_horario)

        # Insertar etiquetas
        if obtener_tipo_sitio.tipo_sitio in ["Hotel", "Restaurante", "Museo"] and arr_etiquetas:
            for cve_etiqueta in arr_etiquetas:
                nueva_relacion = SitioEtiqueta(
                    nuevo_sitio.cve_sitio,
                    cve_etiqueta
                )
                db.session.add(nueva_relacion)
        
        # Insertar imagenes
        fotos = request.files.getlist('fotos_sitio')
        links_imagenes = []
        for foto in fotos:
            if foto.filename != '':
                # VALIDACIONES #
                extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' not in foto.filename and foto.filename.rsplit('.', 1)[1].lower() not in extensiones_validas:
                    raise ValueError("La imagen no tiene una extensión válida. ")
                # SE SUBE LA IMAGEN #
                result = cloudinary.uploader.upload(foto)
                links_imagenes.append(result['secure_url'])
                
                foto_sitio = FotoSitio(
                    link_imagen = result['secure_url'],
                    cve_sitio = nuevo_sitio.cve_sitio,
                    nombre_imagen='x',
                    nombre_autor='x'
                )
                db.session.add(foto_sitio)
        
        # Si todo ha salido bien, confirmamos los cambios
        db.session.commit()

    except Exception as e:
        # Si ha habido algún error, deshacemos los cambios
        db.session.rollback()
        return jsonify({"error": "Hubo un error: " + str(e)}), 400

    return jsonify({"mensaje": "Sitio creado con éxito"}), 201
