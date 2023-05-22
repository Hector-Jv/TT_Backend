from flask import Blueprint, jsonify, request
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

@autenticacion_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    
    ## Datos necesarios ##
    correo = request.form['correo']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    archivo = request.files['imagen']

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
    
    if Validacion.datos_necesarios(archivo) or not Validacion.valor_nulo(archivo):
        nueva_imagen: Imagen = Imagen(
            foto = archivo
        )
        
        if not nueva_imagen.tamaño_permitido() and not nueva_imagen.verificar_extension() and not nueva_imagen.validar_imagen():
            return jsonify({"error": "La imagen ingresada no es válida."}), 400

        nueva_imagen.guardar("IMG_USUARIOS")
        
    ## Creacion de usuario ##
    
    if not Usuario.agregar_usuario(
        correo_usuario = correo,
        usuario = usuario,
        contrasena = contrasena,
        ruta_foto_usuario = nueva_imagen.ruta_foto
    ): 
        return jsonify({"error": "Hubo un error al guardar el usuario en la base de datos. "}), 400

    usuario_encontrado: Usuario = Usuario.obtener_usuario_por_correo(correo)
    
    return jsonify({"usuario": usuario_encontrado.usuario, "correo_usuario": usuario_encontrado.correo}),  201
