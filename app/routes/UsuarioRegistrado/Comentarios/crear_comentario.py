import datetime
from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial, Comentario, FotoComentario
import cloudinary.uploader

crear_comentario_bp = Blueprint('crear_comentario', __name__)

@crear_comentario_bp.route('/crear_comentario', methods=["POST"])
def crear_comentario():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ["correo_usuario", "cve_sitio", "comentario", "calificacion"]
    
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
    print(historial_encontrado.visitado, historial_encontrado.cve_historial)
    if not historial_encontrado.visitado:
        return jsonify({"error": "Debes indicar que ya visitaste el sitio antes de querer hacer una reseña."}), 404
        
    cambio = False
    comentario = None
    calificacion = None
    
    if request.form['comentario']:
        cambio = True
        comentario = request.form['comentario']
        
    print("Comentario: ", comentario)
    if request.form['calificacion']:
        cambio = True
        calificacion = request.form['calificacion']
        if calificacion < 1 or calificacion > 5:
            return jsonify({"error": "La calificación debe estar entre el rango 1 a 5."}), 400
    print("Calificacion: ", calificacion) 
    try:
        nuevo_comentario = Comentario(
            historial_encontrado.cve_historial,
            calificacion,
            comentario
        )
        db.session.add(nuevo_comentario)
        db.session.flush()
    except Exception as e:
        return jsonify({"error": "Hubo un problema con la creación de la reseña.", "mensaje": str(e)}), 400
    
    # Insertar imagenes
    fotos = request.files.getlist('fotos_sitio')
    links_imagenes = []
    for foto in fotos:
        if foto.filename != '':
            # VALIDACIONES #
            extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' not in foto.filename and foto.filename.rsplit('.', 1)[1].lower() not in extensiones_validas:
                raise ValueError("La imagen no tiene una extensión válida. ")
            # SE SUBE LA IMAGEN #
            result = cloudinary.uploader.upload(foto)
            links_imagenes.append(result['secure_url'])
                
            foto_sitio = FotoComentario(
                link_imagen = result['secure_url'],
                cve_comentario = nuevo_comentario.cve_comentario
            )
            cambio = True
            db.session.add(foto_sitio)

    if cambio == False:
        db.session.rollback()
        return jsonify({"mensaje": "No se ha creado el comentario porque no hay contenido."}), 200
                
    db.session.commit()
    return jsonify({"mensaje": "Comentario creado."}), 200