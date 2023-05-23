import os
from os import getcwd
from flask import Blueprint, current_app, jsonify, redirect, request, url_for, send_from_directory
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario, TipoUsuario
from app.classes.validacion import Validacion
from app.classes.imagen import Imagen


autenticacion_bp = Blueprint('autenticacion', __name__)

@autenticacion_bp.route('/login', methods=['POST'])
def inicio_sesion():
    
    ## Datos recibidos del usuario ##
    data = request.get_json()
    correo: str = data.get('correo')
    contrasena: str = data.get('contrasena')
    
    ## Validacion ##
    
    if not Validacion.datos_necesarios(correo, contrasena):
        return jsonify({"error": "Correo y contraseña requeridos."}), 400

    usuario_encontrado: Usuario = Usuario.obtener_usuario_por_correo(correo)
    
    if Validacion.valor_nulo(usuario_encontrado):
        return jsonify({"error": "El correo no se encuentra registrado."}), 404
    
    if not usuario_encontrado.verificar_contrasena(contrasena):
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
    ## Se obtienen los datos del usuario ##
    
    access_token = create_access_token(identity=usuario_encontrado.correo_usuario)
    tipo_usuario: TipoUsuario = TipoUsuario.obtener_tipousuario_por_cve(usuario_encontrado.cve_tipo_usuario)
    
    if tipo_usuario.tipo_usuario == 'Administrador':
        return jsonify({"access_token": access_token, "usuario": usuario_encontrado.usuario, "tipo_usuario": "Administrador"}), 200
    elif tipo_usuario.tipo_usuario == 'Usuario registrado':
        return jsonify({"access_token": access_token, "usuario": usuario_encontrado.usuario, "tipo_usuario": "Usuario registrado"}), 200
    else:
        return jsonify({"error": "No se pudo acceder a la cuenta."}), 403

@autenticacion_bp.route('/registro', methods=['GET','POST'])
def registrar_usuario():
    
    ## Datos necesarios ##
    correo = request.form['correo']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    ## Validaciones ##

    if not Validacion.datos_necesarios(correo, usuario, contrasena):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    if not Validacion.formato_correo(correo):
        return jsonify({"error": "El correo ingresado no es válido."}), 400

    if not Validacion.formato_contrasena(contrasena):
        return jsonify({"error": "La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial."}), 400

    usuario_encontrado: Usuario = Usuario.obtener_usuario_por_correo(correo)
 
    
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
            ruta_foto_usuario = None
    else:
        ruta_foto_usuario = None
        
    ## Creacion de usuario ##
    
    if not Usuario.agregar_usuario(
        correo_usuario = correo,
        usuario = usuario,
        contrasena = contrasena,
        nombre_imagen = nombre_imagen
    ): 
        return jsonify({"error": "Hubo un error al guardar el usuario en la base de datos. "}), 400

    usuario_encontrado: Usuario = Usuario.obtener_usuario_por_correo(correo)
    
    return ({"correo_usuario": usuario_encontrado.correo_usuario, "mensaje": "Te has registrado con exito"}),  201


from flask import send_from_directory

PATH_FILE = getcwd() + "/static/usuarios/"

@autenticacion_bp.route('/img_usuario/<string:nombre_imagen>')  
def obtener_imagen(nombre_imagen):
    # nombre_imagen debe tener este formato: /nombre_usuario/nombre_foto
    return send_from_directory(PATH_FILE, path=nombre_imagen, as_attachment=False)


    