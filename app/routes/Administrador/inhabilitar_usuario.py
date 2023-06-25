from flask import Blueprint, jsonify
from app import db
from app.models import Usuario

inhabilitar_usuario_bp = Blueprint('inhabilitar_usuario', __name__)

@inhabilitar_usuario_bp.route('/inhabilitar_usuario/<string:correo_usuario>', methods=['PUT'])
def inhabilitar_usuario(correo_usuario):
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    
    if not usuario_encontrado:
        return jsonify({"error": "No se encontró el usuario."}), 400
    
    if usuario_encontrado.habilitado:
        usuario_encontrado.habilitado = False
        return jsonify({"mensaje": f"Usuario {usuario_encontrado.usuario} a sido inhabilitado."}), 200
    else:
        usuario_encontrado.habilitado = True
        return jsonify({"mensaje": f"Usuario {usuario_encontrado.usuario} a sido habilitado."}), 200
