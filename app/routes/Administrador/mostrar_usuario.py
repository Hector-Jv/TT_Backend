from flask import Blueprint, jsonify, request
from app.models import Usuario, Historial, Comentario, FotoComentario
from app import db
from datetime import datetime

mostrar_usuario_bp = Blueprint('mostrar_usuario', __name__)

@mostrar_usuario_bp.route('/mostrar_usuario/<string:correo_usuario>', methods=["GET"])
def mostrar_usuario(correo_usuario):
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    
    if not usuario_encontrado:
        return jsonify({"error": "No se encontró el usuario."}), 400
    
    reseñas = []
    historiales_encontrados = Historial.query.filter_by(correo_usuario=correo_usuario).all()
    for historial in historiales_encontrados:
        comentario_encontrado = Comentario.query.filter_by(cve_historial=historial.cve_historial).first()
        if not comentario_encontrado:
            continue
        
        comentario_dict = {}
        comentario_dict["fotos"] = []
        fotos = FotoComentario.query.filter_by(cve_comentario=Comentario.cve_comentario).all()
        if fotos:
            for foto in fotos:
                comentario_dict["fotos"].append(foto.link_imagen)
        comentario_dict["comentario"] = comentario_encontrado.comentario
        comentario_dict["calificacion"] = comentario_encontrado.calificacion
        comentario_dict["fecha"] = comentario_encontrado.fecha_comentario
        reseñas.append(comentario_dict)
        
    return jsonify(reseñas), 200
