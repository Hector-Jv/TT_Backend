import json
from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Colonia, TipoSitio, SitioEtiqueta, FotoSitio, ServicioHotel, Usuario, TipoUsuario
import cloudinary.uploader

crear_sitio_bp = Blueprint('crear_sitio', __name__)

@crear_sitio_bp.route('/crear_sitio', methods=['POST'])
def crear_sitio(): 

    ## VALIDACIONES DE ENTRADA ## 

    identificadores = ["correo_usuario", "nombre_sitio",
                       "longitud", "latitud",
                       "descripcion", "correo",
                       "costo", "pagina_web",
                       "telefono", "adscripcion",
                       "cve_tipo_sitio", "cve_delegacion",
                       "colonia", "etiquetas", "servicios"]

    for id in identificadores:
        if id not in request.form:
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400

    # Obligatorios #
    correo_usuario = request.form["correo_usuario"]
    nombre_sitio = request.form["nombre_sitio"]
    longitud = float(request.form["longitud"])
    latitud = float(request.form["latitud"])
    cve_tipo_sitio = int(request.form["cve_tipo_sitio"]) 
    cve_delegacion = int(request.form["cve_delegacion"])
    colonia = request.form["colonia"]
    # Opcionales #
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
    
    obligatorios = {
        "correo_usuario": request.form["correo_usuario"],
        "nombre_sitio": request.form["nombre_sitio"],
        "longitud": float(request.form["longitud"]),
        "latitud": float(request.form["latitud"]),
        "cve_tipo_sitio": int(request.form["cve_tipo_sitio"]),
        "cve_delegacion": int(request.form["cve_delegacion"]),
        "colonia": request.form["colonia"]
    }

    for nombre, valor in obligatorios.items():
        if not valor:
            return jsonify({"error": f"Es necesario mandar un valor valido en {nombre}."}), 400
        
    ## VALIDACIÓN DE PERMISOS ##
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
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
        
    # Insertar colonia
    obtener_colonia = Colonia.query.filter_by(nombre_colonia=colonia).first()
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
        
    # Insertar etiquetas
    if arreglo_etiquetas and obtener_tipo_sitio.tipo_sitio in ["Restaurante", "Museo"]:
        for etiqueta in arreglo_etiquetas:
            nueva_relacion = SitioEtiqueta(
                nuevo_sitio.cve_sitio,
                etiqueta["cve_etiqueta"]
            )
            db.session.add(nueva_relacion)
            
    if arreglo_servicios and obtener_tipo_sitio.tipo_sitio == "Hotel":
        for servicio in arreglo_servicios:
            nueva_relacion = ServicioHotel(
                nuevo_sitio.cve_sitio,
                servicio["cve_servicio"]
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



