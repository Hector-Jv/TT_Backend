from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db
from app.models import Usuario, TipoUsuario
from app.utils.validaciones import datos_necesarios


login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def inicio_sesion():
    
    # Datos recibidos del usuario.
    data = request.get_json()

    # Se extraen los datos recibidos del usuario.
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    
    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(correo, contrasena):
        return jsonify({"error": "Correo y contraseña requeridos."}), 400

    # Busca si el correo del usuario se encuentra registrado.
    usuario = Usuario.query.filter_by(correo_usuario=correo).first()

    # Se verifica que este registrado el usuario en la base de datos.
    if usuario is None:
        return jsonify({"error": "Correo no encontrado"}), 404
    
    # Se verifica que la contraseña ingresada coincida con la registrada en la base de datos.
    if usuario.contrasena != contrasena:
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
    # Se crea un token de acceso que utiliza el correo del usuario como identificador único (flask_jwt_extended)
    access_token = create_access_token(identity=usuario.correo_usuario)
    
    # Busca el tipo de usuario que pertenece el usuario.
    tipo_usuario = TipoUsuario.query.filter_by(cve_tipo_usuario=usuario.cve_tipo_usuario).first()
    
    
    if tipo_usuario.tipo_usuario == 'Administrador':
        return jsonify({"access_token": access_token, "usuario": usuario.usuario, "tipo_usuario": "Administrador"}), 200
    elif tipo_usuario.tipo_usuario == 'Usuario registrado':
        return jsonify({"access_token": access_token, "usuario": usuario.usuario, "tipo_usuario": "Usuario registrado"}), 200
    else:
        return jsonify({"error": "No se puede acceder a la cuenta."}), 403


