from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.imagen import Imagen
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio, Historial, Calificacion, CalificacionHotel, CalificacionRestaurante, Comentario, FotoComentario
from app.classes.validacion import Validacion
from app.classes.modificar_sitio import modificar_sitio

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
    costo = float(costo)
    cve_tipo_sitio = arr_tipo_sitio["value"]
    arr_etiquetas = [etiqueta["value"] for etiqueta in arr_etiquetas]
    cve_delegacion = arr_delegacion["value"]
    
    # Validaciones #
    if Sitio.query.filter_by(nombre_sitio=nombre_sitio, x_longitud=longitud, y_latitud=latitud).first():
        return jsonify({"error": "Ya existe un sitio con ese nombre y con la misma dirección."}), 400
        
    # Inserciones #
    obtener_colonia = Colonia.query.filter_by(nombre_colonia=colonia).first()
    if not obtener_colonia:
        crear_colonia = Colonia(colonia, cve_delegacion)
        db.session.add(crear_colonia)
        obtener_colonia = crear_colonia
    
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
    
    try:
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
            calificacion = calificacion_sitio
            )
        db.session.add(nuevo_sitio)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Hubo un error al tratar de crear el sitio de interés."}), 400
        
    try:
        for horario in arr_horario:
            nuevo_horario = Horario(
                horario["dia"],
                horario["horario_apertura"],
                horario["horario_cierre"],
                horario["cve_sitio"]
            )
            db.session.add(nuevo_horario)
    except Exception in e:
        db.session.rollback()
        return jsonify({"error": "Hubo un error al tratar de agregar los horarios del sitio."}), 400
    
    if obtener_tipo_sitio.tipo_sitio in ["Hotel", "Restaurante", "Museo"]:
        try:
            for cve_etiqueta in arr_etiquetas:
                nueva_relacion = SitioEtiqueta(
                    nuevo_sitio.cve_sitio,
                    cve_etiqueta
                )
                db.session.add(nueva_relacion)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Hubo un error al tratar de agregar las etiqueta del sitio."}), 400
    
    """
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
    """
    db.session.commit()
    return jsonify({"mensaje": "Sitio creado con éxito"}), 201
