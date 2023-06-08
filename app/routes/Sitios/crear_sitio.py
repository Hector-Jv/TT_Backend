import json
from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Colonia, Horario, TipoSitio, SitioEtiqueta, FotoSitio
from app.classes.modificar_sitio import modificar_sitio
import cloudinary.uploader

crear_sitio_bp = Blueprint('crear_sitio', __name__)

@crear_sitio_bp.route('/crear_sitio', methods=['POST'])
def crear_sitio(): 
    # Datos ingresados #
    try:
        # Modelo Sitio
        nombre_sitio = request.form["nombre_sitio"]
        longitud = float(request.form["longitud"])
        latitud = float(request.form["latitud"])
        descripcion = request.form["descripcion"]
        correo = request.form["correo"]
        costo = float(request.form["costo"])
        pagina_web = request.form["pagina_web"]
        telefono = request.form["telefono"]
        adscripcion = request.form["adscripcion"]
        cve_tipo_sitio = int(request.form["cve_tipo_sitio"]) 
        cve_delegacion = int(request.form["cve_delegacion"])
        colonia = request.form["colonia"]
        
        # Modelo SitioEtiqueta #
        arreglo_etiquetas = request.form["etiquetas"]
        
        # Modelo Horario
        arreglo_horario = request.form["horarios"]
        
    except Exception as e:
        return jsonify({"error": f"Hubo un error al recibir los datos: {e}"}), 400
    
    if arreglo_etiquetas:
        arreglo_etiquetas = json.loads(arreglo_etiquetas)
    if arreglo_horario:
        arreglo_horario = json.loads(arreglo_horario)
    
    
    # Validaciones #
    if Sitio.query.filter_by(nombre_sitio=nombre_sitio).first():
        return jsonify({"error": "Ya existe un sitio con ese nombre y con la misma dirección."}), 400
    
    
    obtener_tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
    obtener_colonia = Colonia.query.filter_by(nombre_colonia=colonia).first()
    
    
    # Insertar colonia
    if not obtener_colonia:
        crear_colonia = Colonia(
            colonia, 
            cve_delegacion
        )
        db.session.add(crear_colonia)
        db.session.flush()
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
        calificacion = None
    )
    db.session.add(nuevo_sitio)
    db.session.flush()
        
    # Insertar horarios
    for horario in arreglo_horario:
        nuevo_horario = Horario(
            horario["dia"],
            horario["horaEntrada"],
            horario["horaSalida"],
            nuevo_sitio.cve_sitio    
        )
        db.session.add(nuevo_horario)
        
    # Insertar etiquetas
    if obtener_tipo_sitio.tipo_sitio in ["Restaurante", "Museo"] and arreglo_etiquetas:
        for cve_etiqueta in arreglo_etiquetas:
            nueva_relacion = SitioEtiqueta(
                nuevo_sitio.cve_sitio,
                cve_etiqueta["cve_etiqueta"]
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
                cve_sitio = nuevo_sitio.cve_sitio
            )
            db.session.add(foto_sitio)
        
    # Si todo ha salido bien, confirmamos los cambios
    db.session.commit()
    return jsonify({"mensaje": "Sitio creado con éxito"}), 201



