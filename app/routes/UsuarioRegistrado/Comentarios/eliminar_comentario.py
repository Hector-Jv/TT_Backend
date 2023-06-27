import datetime
from flask import Blueprint, jsonify, request
from app import db
from app.models import Historial, Comentario, FotoComentario, Sitio

eliminar_comentario_bp = Blueprint('eliminar_comentario', __name__)

@eliminar_comentario_bp.route('/eliminar_comentario', methods=["DELETE"])
def eliminar_comentario():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ['correo_usuario', 'cve_sitio']
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    correo_usuario = data.get('correo_usuario')
    cve_sitio = data.get('cve_sitio')
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    if not cve_sitio or not isinstance(cve_sitio, int):
        return jsonify({"error": "Es necesario mandar un valor valido en cve_sitio."}), 400
    
    
    ## ELIMINACION DE RESEÑA ##
    historial_encontrado: Historial = Historial.query.filter_by(correo_usuario=correo_usuario, cve_sitio=cve_sitio).first()
    if not historial_encontrado:
        return jsonify({"error": "No se encontró registro de historial"}), 404
    
    comentario_encontrado: Comentario = Comentario.query.filter_by(cve_historial=historial_encontrado.cve_historial).first()
    if not comentario_encontrado:
        return jsonify({"error": "No se encontró comentario del sitio."}), 404
    
    fotos_encontradas = FotoComentario.query.filter_by(cve_comentario=comentario_encontrado.cve_comentario).all()
    if fotos_encontradas:
        for foto in fotos_encontradas:
            db.session.delete(foto)
            db.session.flush()
    
    ## SE ACTUALIZA LA INFORMACIÓN DEL SITIO ##
    sitio_encontrado:Sitio = Sitio.query.get(cve_sitio)
    
    if sitio_encontrado.num_calificaciones == 1 and comentario_encontrado.calificacion != None:
        sitio_encontrado.num_calificaciones = 0
        sitio_encontrado.calificacion = None
    elif sitio_encontrado.num_calificaciones > 1 and comentario_encontrado.calificacion != None:
        sitio_encontrado.calificacion = ((sitio_encontrado.calificacion * sitio_encontrado.num_calificaciones) - comentario_encontrado.calificacion) / (sitio_encontrado.num_calificaciones - 1)
        sitio_encontrado.num_calificaciones -= 1
    
    
    db.session.delete(comentario_encontrado)
    db.session.commit()
    
        
    return jsonify({"mensaje": "Se ha eliminado el comentario correctamente."}), 200