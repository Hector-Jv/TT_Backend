from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial, Comentario

agregar_historial_bp = Blueprint('agregar_historial', __name__)

@agregar_historial_bp.route('/agregar_historial', methods=["POST"])
def agregar_historial():
    
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
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 400
    
    mensaje = ""
    historial_encontrado: Historial = Historial.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario, cve_sitio=cve_sitio).first()
    if not historial_encontrado:
        nuevo_historial = Historial(
            usuario_encontrado.correo_usuario,
            cve_sitio
        )
        db.session.add(nuevo_historial)
        db.session.commit()
        mensaje = "Añadido a visitados."
        sitios_visitados = Historial.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario, visitado=True).all()
        arreglo_visitados = [sitio.cve_sitio for sitio in sitios_visitados]
        return jsonify({"sitios_visitados": arreglo_visitados, "sitio_modificado": cve_sitio, "mensaje": mensaje}), 200
        
    try:
        if historial_encontrado.visitado:
            comentario_encontrado: Comentario = Comentario.query.filter_by(cve_historial=historial_encontrado.cve_historial).first()
            if comentario_encontrado:
                return jsonify({"error": "Elimina los comentarios realizados antes de indicar que no has visitado el sitio."}), 400
            historial_encontrado.visitado = False
            db.session.commit()
            mensaje = "Quitado de visitados."
            
        else:
            historial_encontrado.visitado = True
            db.session.commit()
            mensaje = "Añadido de visitados."
            
    except Exception as e:
        return jsonify({"error": "Hubo un error al añadir/quitar de visitados."}), 400
    
    sitios_visitados = Historial.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario, visitado=True).all()
    arreglo_visitados = [sitio.cve_sitio for sitio in sitios_visitados]
    return jsonify({"sitios_visitados": arreglo_visitados, "sitio_modificado": cve_sitio, "mensaje": mensaje}), 200
        