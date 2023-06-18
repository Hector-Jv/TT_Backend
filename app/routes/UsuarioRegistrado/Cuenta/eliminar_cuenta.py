import datetime
from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Usuario, Historial, Comentario

eliminar_cuenta_bp = Blueprint('eliminar_cuenta', __name__)

@eliminar_cuenta_bp.route('/eliminar_cuenta', methods=["DELETE"])
def eliminar_cuenta():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ['correo_usuario', 'contrasena']
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    correo_usuario = data.get('correo_usuario')
    contrasena = data.get('contrasena')
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    if not contrasena or not isinstance(contrasena, str):
        return jsonify({"error": "Es necesario mandar un valor valido en contrasena."}), 400
    
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 404
    
    if not usuario_encontrado.verificar_contrasena(contrasena):
        return jsonify({"error": "Contraseña incorrecta."}), 400
    
    return jsonify({"mensaje": "todo bien"}), 200