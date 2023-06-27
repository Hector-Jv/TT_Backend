from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial, Comentario, FotoComentario, Sitio

mostrar_reseña_bp = Blueprint('mostrar_reseña', __name__)

@mostrar_reseña_bp.route('/mostrar_reseñas/<string:correo_usuario>')
def mostrar_reseñas(correo_usuario):
    
    if not correo_usuario:
        return jsonify({"error": "Es necesario ingresar un correo."}), 400
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "No se encontró una cuenta asociada con ese correo."}), 404
    
    historiales = Historial.query.filter_by(correo_usuario = correo_usuario).all()
    if not historiales:
        return jsonify([]), 200
    
    reseñas_usuario = []
    for historial in historiales:
        sitio_reseña = {}
        comentario_encontrado: Comentario = Comentario.query.filter_by(cve_historial=historial.cve_historial).first()
        if not comentario_encontrado:
            continue
        
        sitio_encontrado: Sitio = Sitio.query.get(historial.cve_sitio)
        sitio_reseña["cve_sitio"] = historial.cve_sitio
        sitio_reseña["nombre_sitio"] =sitio_encontrado.nombre_sitio
        sitio_reseña["comentario"] = comentario_encontrado.comentario
        sitio_reseña["calificacion"] = comentario_encontrado.calificacion
        sitio_reseña["fecha"] = historial.fecha_visita
        fotos_encontradas = FotoComentario.query.filter_by(cve_comentario=comentario_encontrado.cve_comentario).all()
        fotos = []
        if fotos_encontradas:
            for foto in fotos_encontradas:
                fotos.append(foto.link_imagen)
        sitio_reseña["foto"] = fotos
        reseñas_usuario.append(sitio_reseña)
        
    return jsonify(reseñas_usuario), 200
        