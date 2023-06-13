import re
from os import getcwd
from flask import Blueprint, current_app, jsonify, request
from app import db
from app.models import Usuario
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
        db.session.commit()
    except Exception as e:
        return jsonify({"mensaje": "Error al crear al usuario"}), 400
    
    return jsonify({
        "correo_usuario": nuevo_usuario.correo_usuario,
        "usuario": nuevo_usuario.usuario,
        "cve_tipo_usuario": nuevo_usuario.cve_tipo_usuario,
        "link_imagen": nuevo_usuario.link_imagen
    }), 200
      