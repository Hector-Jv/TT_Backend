import os
from os import getcwd
from flask import Blueprint, current_app, jsonify, request, send_from_directory
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario, TipoUsuario
from app.classes.validacion import Validacion
from app.classes.imagen import Imagen

registrar_usuario_bp = Blueprint('Registrar usuario', __name__)

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

    if 'foto_usuario' in request.files:
        archivo = request.files['foto_usuario']
        print("Archivo: ", archivo)
        if archivo.filename != '':
            
            if not Imagen.verificar_extension(archivo):
                return jsonify({"error": "La imagen no tiene una extensión válida. "}), 400
            
            if not Imagen.tamaño_permitido(archivo):
                return jsonify({"error": "La imagen es demasiado grande. "}), 400
            
            if not Imagen.validar_imagen(archivo):
                return jsonify({"error": "Hubo un problema al intentar abrir la imagen. "}), 400
            
            nombre_imagen = Imagen.guardar(foto=archivo, nombre=usuario, ruta="IMG_USUARIOS")

        else:
            nombre_imagen = None
    else:
        nombre_imagen = None
        
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

