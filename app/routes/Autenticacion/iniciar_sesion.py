from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario, TipoUsuario
from app.classes.validacion import Validacion

iniciar_sesion_bp = Blueprint('Iniciar sesion', __name__)

@iniciar_sesion_bp.route('/login', methods=['POST'])
def inicio_sesion():
    
    ## Datos recibidos del usuario ##
    data = request.get_json()
    correo: str = data.get('correo')
    contrasena: str = data.get('contrasena')
    
    ## Validacion ##
    if not correo or not contrasena:
        return jsonify({"error": "Correo y contraseña requeridos."}), 400

    usuario_encontrado: Usuario = Usuario.query.get(correo)
    if usuario_encontrado is None:
        return jsonify({"error": "El correo no se encuentra registrado."}), 404
    if not usuario_encontrado.verificar_contrasena(contrasena):
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
    ## Se obtienen los datos del usuario ##
    access_token = create_access_token(identity=usuario_encontrado.correo_usuario)
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    
    if tipo_usuario.tipo_usuario == 'Administrador' or tipo_usuario.tipo_usuario == 'Usuario registrado':
        return jsonify({"access_token": access_token, "usuario": usuario_encontrado.usuario, "tipo_usuario": tipo_usuario.tipo_usuario, "link_imagen": usuario_encontrado.link_imagen}), 200
    else:
        return jsonify({"error": "No se pudo acceder a la cuenta."}), 403
