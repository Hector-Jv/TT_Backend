import os, re
from os import getcwd
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario, TipoUsuario

registrar_usuario_bp = Blueprint('Registrar usuario', __name__)

"""
@registrar_usuario_bp.route('/registro', methods=['GET','POST'])
def registrar_usuario():
    
    ## Datos necesarios ##
    correo = request.form['correo']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    ## Validaciones ##

    if not correo or not usuario or not contrasena:
        return jsonify({"error": "Hacen falta datos."}), 400
    
    if not Validacion.formato_correo(correo):
        return jsonify({"error": "El correo ingresado no es válido."}), 400

    if not Validacion.formato_contrasena(contrasena):
        return jsonify({"error": "La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial."}), 400

    usuario_encontrado: Usuario = Usuario.query.get(correo)
 
    if not Validacion.valor_nulo(usuario_encontrado):
        return jsonify({"error": "Ya existe el correo ingresado."}), 404
    
    usuario_encontrado: Usuario = Usuario.obtener_usuario_por_usuario(usuario)
    
    if not Validacion.valor_nulo(usuario_encontrado):
        return jsonify({"error": "Ya existe el usuario ingresado."}), 404
 
    ## Manejo de imagen ##

    ## MANEJO DE IMAGEN ##
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
    
        
    ## Creacion de usuario ##
    
    if not Usuario.agregar_usuario(
        correo_usuario = correo,
        usuario = usuario,
        contrasena = contrasena,
        nombre_imagen = nombre_imagen
    ): 
        return jsonify({"error": "Hubo un error al guardar el usuario en la base de datos. "}), 400

    usuario_encontrado: Usuario = Usuario.obtener_usuario_por_correo(correo)

    ## Se obtienen los datos del usuario ##
    access_token = create_access_token(identity=usuario_encontrado.correo_usuario)
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    
    return jsonify({
        "access_token": access_token, 
        "usuario": usuario_encontrado.usuario, 
        "tipo_usuario": tipo_usuario.tipo_usuario, 
        "foto": usuario_encontrado.nombre_imagen
    }), 200
"""

import cloudinary.uploader
@registrar_usuario_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    
    ## DATOS ##
    correo = request.form['correo']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    
    ## VALIDACIONES ##
    if not correo or not usuario or not contrasena:
        return jsonify({"error": "Hacen falta datos."}), 400
    
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
            
    ## Creacion de usuario ##
    
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

    ## Se obtienen los datos del usuario ##
    access_token = create_access_token(identity=nuevo_usuario.correo_usuario)
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(nuevo_usuario.cve_tipo_usuario)
    
    return jsonify({
        "access_token": access_token, 
        "usuario": nuevo_usuario.usuario, 
        "tipo_usuario": tipo_usuario.tipo_usuario, 
        "link_imagen": link_foto
    }), 200
      

"""
    fotos = request.files.getlist('foto_usuario')

    for foto in fotos:
        if foto.filename != '':
            # VALIDACIONES #
            extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' not in foto.filename and foto.filename.rsplit('.', 1)[1].lower() not in extensiones_validas:
                return jsonify({"error": "La imagen no tiene una extensión válida. "}), 400
            
            # SE SUBE LA IMAGEN #
            result = cloudinary.uploader.upload(foto)
            print(result)
            print("Nombre de imagen: ", result['original_filename'])
            print("URL: ", result['secure_url'])
    """