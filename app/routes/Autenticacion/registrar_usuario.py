import json
import re
from os import getcwd
from flask import Blueprint, current_app, jsonify, request
from app import db
from app.models import Usuario, TipoUsuario, UsuarioEtiqueta, UsuarioServicio
import cloudinary.uploader

registrar_usuario_bp = Blueprint('Registrar usuario', __name__)

@registrar_usuario_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ['correo', 'usuario', 'contrasena']
    
    for id in identificadores:
        if id not in request.form:
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400

    correo = request.form['correo']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    
    obligatorios = {
        "correo": request.form['correo'],
        "usuario": request.form['usuario'],
        "contrasena": request.form['contrasena']
    }
    
    for nombre, valor in obligatorios.items():
        if not valor:
            return jsonify({"error": f"Es necesario mandar un valor valido en {nombre}."}), 400
    
    formato_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(formato_correo, correo):
        return jsonify({"error": "El correo ingresado no es válido."}), 400

    formato_contrasena = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$'
    if not re.match(formato_contrasena, contrasena):
        return jsonify({"error": "La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial."}), 400

    if Usuario.query.get(correo):
        return jsonify({"error": "Ya existe el correo ingresado."}), 404
    
    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({"error": "Ya existe el usuario ingresado."}), 404

    ## MANEJO DE IMAGEN ##
    link_foto = None
    if 'foto_usuario' in request.files:
        foto = request.files['foto_usuario']
        if foto.filename != '':
            # VALIDACIONES #
            extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
            if not '.' in foto.filename and not foto.filename.rsplit('.', 1)[1].lower() in extensiones_validas:
                return jsonify({"error": "La imagen no tiene una extensión válida. "}), 400
            
            # SE SUBE LA IMAGEN #
            upload_result = cloudinary.uploader.upload(foto)
            link_foto = upload_result['secure_url']
    
    try:
        nuevo_usuario = Usuario(
            correo_usuario = correo,
            usuario = usuario,
            contrasena = contrasena,
            link_imagen = link_foto
        )
        db.session.add(nuevo_usuario)
        db.session.flush()
        # db.session.commit()
    except Exception as e:
        return jsonify({"mensaje": "Error al crear al usuario"}), 400
    
    tipo_usuario_encontrado: TipoUsuario = TipoUsuario.query.get(nuevo_usuario.cve_tipo_usuario)
    
    arreglo_etiquetas = request.form["etiquetas"]
    arreglo_servicios = request.form["servicios"]
    
    if arreglo_etiquetas:
        arreglo_etiquetas = json.loads(arreglo_etiquetas)
    if arreglo_servicios:
        arreglo_servicios = json.loads(arreglo_servicios)
    
    try:
        for etiqueta in arreglo_etiquetas:
            usuario_etiqueta_nuevo: UsuarioEtiqueta = UsuarioEtiqueta(
                nuevo_usuario.correo_usuario,
                etiqueta["label"]
            )
            db.session.add(usuario_etiqueta_nuevo)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error en agregar las preferencias del usuario (etiquetas)."}), 400
    
    try:
        for servicio in arreglo_servicios:
            usuario_servicio_nuevo: UsuarioServicio = UsuarioServicio(
                nuevo_usuario.correo_usuario,
                servicio["label"]
            )
            db.session.add(usuario_servicio_nuevo)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error en agregar las preferencias del usuario (servicios)."}), 400

    db.session.commit()

    return jsonify({
        "correo_usuario": nuevo_usuario.correo_usuario,
        "usuario": nuevo_usuario.usuario,
        "cve_tipo_usuario": nuevo_usuario.cve_tipo_usuario,
        "tipo_usuario": tipo_usuario_encontrado.tipo_usuario,
        "link_imagen": nuevo_usuario.link_imagen,
        "servicios": [servicio.cve_servicio for servicio in UsuarioServicio.query.filter_by(correo_usuario=nuevo_usuario.correo_usuario).all()],
        "etiquetas": [etiqueta.cve_etiqueta for etiqueta in UsuarioEtiqueta.query.filter_by(correo_usuario=nuevo_usuario.correo_usuario).all()]
    }), 200
    