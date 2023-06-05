from flask import Blueprint, jsonify
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Usuario, Historial

agregar_favorito_bp = Blueprint('agregar_favorito', __name__)

@agregar_favorito_bp.route('/agregar_sitio_favorito/<int:cve_sitio>', methods=["POST"])
@jwt_required()
def agregar_sitio_favorito(cve_sitio):
    
    identificador_usuario = get_jwt_identity()
    usuario:Usuario = Usuario.query.get(identificador_usuario)
    
    if not usuario:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 404
    
    historial_encontrado: Historial = Historial.query.filter_by(cve_usuario=usuario.correo_usuario, cve_sitio=cve_sitio).first()
    
    if historial_encontrado.me_gusta:
        historial_encontrado.me_gusta = False
        db.session.commit()
        return jsonify({"mensaje": "Quitado de favoritos."}), 200
    else:
        historial_encontrado.me_gusta = True
        db.session.commit()
        return jsonify({"mensaje": "Añadido a favoritos."}), 200
        
    