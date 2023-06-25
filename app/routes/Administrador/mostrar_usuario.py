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
    
    info = {}
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
                foto_dict = {}
                foto_dict["cve_foto"] = foto.cve_foto_comentario
                foto_dict["link"] = foto.link_imagen
                comentario_dict["fotos"].append(foto_dict)
        comentario_dict["cve_comentario"] = comentario_encontrado.cve_comentario
        comentario_dict["comentario"] = comentario_encontrado.comentario
        comentario_dict["calificacion"] = comentario_encontrado.calificacion
        comentario_dict["fecha"] = comentario_encontrado.fecha_comentario
        reseñas.append(comentario_dict)
        
    info["reseñas"] = reseñas
    info["correo"] = correo_usuario
    info["usuario"] = usuario_encontrado.usuario
    info["habilitado"] = usuario_encontrado.habilitado
    return jsonify(info), 200
