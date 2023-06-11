import datetime
from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial, Comentario

crear_comentario_bp = Blueprint('crear_comentario', __name__)

@crear_comentario_bp.route('/crear_comentario', methods=["POST"])
def crear_comentario():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ['correo_usuario', 'cve_sitio']
    
    for id in identificadores:
        if id not in request.form:
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    obligatorios = {
        "correo_usuario": request.form['correo_usuario'],
        "cve_sitio": request.form['cve_sitio']
    }
    
    usuario_encontrado: Usuario = Usuario.query.get(obligatorios["correo_usuario"])
    if not usuario_encontrado:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 404
    
    
    
    historial_encontrado: Historial = Historial.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario, 
                                                                cve_sitio=obligatorios["cve_sitio"]).first()
    
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