from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial

agregar_favorito_bp = Blueprint('agregar_favorito', __name__)

@agregar_favorito_bp.route('/agregar_sitio_favorito', methods=["POST"])
def agregar_sitio_favorito():
    
    try:
        data = request.get_json()
        correo_usuario = data.get('correo_usuario')
        cve_sitio = data.get('cve_sitio')
        
        usuario: Usuario = Usuario.query.get(correo_usuario)
        
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
    except Exception as e:
        print("Error: ", e)        
        