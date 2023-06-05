import datetime
from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Usuario, Historial, Comentario

crear_comentario_bp = Blueprint('crear_comentario', __name__)

@crear_comentario_bp.route('/crear_comentario', methods=["POST"])
@jwt_required()
def crear_comentario():
    
    identificador_usuario = get_jwt_identity()
    usuario: Usuario = Usuario.query.get(identificador_usuario)
    
    if not usuario:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 404
    
    # Datos ingresados #
    try:
        cve_sitio = request.form["cve_sitio"]
        comentario = request.form["comentario"]
    except Exception as e:
        return jsonify({"mensaje": "Hubo un problema con la inserción de los datos."}), 400
    
    historial_encontrado: Historial = Historial.query.filter_by(cve_usuario=usuario.correo_usuario, cve_sitio=cve_sitio).first()
    
    try:
        nuevo_comentario = Comentario(
            comentario,
            datetime.now(),
            historial_encontrado.cve_historial
        )
        db.session.add(nuevo_comentario)
    except Exception as e:
        return jsonify({"mensaje": "Hubo un problema con la creación de la reseña."}), 400
    
    ###############
    """
    FALTAN LAS IMAGENES
    """
    ###############
    
    return jsonify({"mensaje": "Por terminar"}), 200