from app import db
from flask import Blueprint, jsonify, request
from app.models import Comentario, FotoComentario

comentario_bp = Blueprint('comentarios', __name__)


@comentario_bp.route('/crear_comentario', methods=['POST'])
def crear_comentario():
    # Asumiendo que el contenido del comentario viene en el cuerpo de la solicitud
    contenido = request.form['contenido']
    
    comentario = Comentario(contenido=contenido) # Asumiendo que tu modelo Comentario tiene un campo 'contenido'
    db.session.add(comentario)
    db.session.commit()

    return jsonify({'cve_comentario': comentario.cve_comentario}), 201

@comentario_bp.route('/subir_foto/<int:cve_comentario>', methods=['POST'])
def subir_foto(cve_comentario):
    if 'foto' not in request.files:
        return 'No se encontró ninguna foto en el formulario', 400

    foto = request.files['foto']
    resultado, codigo = FotoComentario.guardar_imagen(foto, cve_comentario)

    return resultado, codigo

@comentario_bp.route('/obtener_fotos/<int:cve_comentario>', methods=['GET'])
def obtener_fotos(cve_comentario):
    rutas_fotos = FotoComentario.obtener_fotos_por_comentario(cve_comentario)
    return jsonify(rutas_fotos), 200


@comentario_bp.route('/eliminar_foto/<int:cve_foto_comentario>', methods=['DELETE'])
def eliminar_foto(cve_foto_comentario):
    resultado = FotoComentario.eliminar_foto(cve_foto_comentario)
    return resultado, 200 if resultado == 'Foto eliminada exitosamente.' else 404

@comentario_bp.route('/eliminar_fotos_comentario/<int:cve_comentario>', methods=['DELETE'])
def eliminar_fotos_comentario(cve_comentario):
    resultado = FotoComentario.eliminar_fotos_comentario(cve_comentario)
    return resultado, 200 if resultado == 'Fotos eliminadas exitosamente.' else 404
