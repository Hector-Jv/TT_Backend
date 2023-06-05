import datetime
from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Usuario, Historial, Comentario

eliminar_cuenta_bp = Blueprint('eliminar_cuenta', __name__)

@eliminar_cuenta_bp.route('/eliminar_cuenta', methods=["POST"])
@jwt_required()
def eliminar_cuenta():
    
    identificador_usuario = get_jwt_identity()
    usuario: Usuario = Usuario.query.get(identificador_usuario)
    
    if not usuario:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 404
    
    
    ###############
    """
    POR TERMINAR
    """
    ###############
    
    return jsonify({"mensaje": "Por terminar"}), 200