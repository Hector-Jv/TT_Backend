import datetime, random, string
from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial, Comentario, FotoComentario

eliminar_cuenta_bp = Blueprint('eliminar_cuenta', __name__)

@eliminar_cuenta_bp.route('/eliminar_cuenta', methods=["DELETE"])
def eliminar_cuenta():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ['correo_usuario', 'contrasena']
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    correo_usuario = data.get('correo_usuario')
    contrasena = data.get('contrasena')
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    if not contrasena or not isinstance(contrasena, str):
        return jsonify({"error": "Es necesario mandar un valor valido en contrasena."}), 400
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Necesitas iniciar sesión para realizar la acción."}), 404
    
    if not usuario_encontrado.verificar_contrasena(contrasena):
        return jsonify({"error": "Contraseña incorrecta."}), 400
    
    
    # Creación de usuario ficticio #
    dominio = "@ficticio.com"
    caracteres = string.ascii_lowercase + string.digits  # Letras minúsculas y dígitos
    correo = ''.join(random.sample(caracteres, 20)) + dominio
    
    try:
        usuario_ficticio: Usuario = Usuario(
            correo,
            caracteres,
            caracteres
        )
        db.session.add(usuario_ficticio)
        db.session.flush()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo crear el usuario ficticio", "problema": str(e)}), 400
    
    try:
        historiales_encontrados = Historial.query.filter_by(correo_usuario = usuario_encontrado).all()
        if historiales_encontrados:
            for historial in historiales_encontrados:
                historial.correo_usuario = usuario_ficticio.correo_usuario
                
                comentario_encontrado = Comentario.query.filter_by(cve_historial = historial.cve_historial).first()
                if comentario_encontrado:
                    fotos_encontradas = FotoComentario.query.filter_by(cve_comentario = comentario_encontrado.cve_comentario).all()
                    if fotos_encontradas:
                        for foto in fotos_encontradas:
                            db.session.delete(foto)
                db.session.delete(comentario_encontrado)
                
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo crear el usuario ficticio", "problema": str(e)})
    
    
    
    
    db.session.commit()
        
    return jsonify({"usuario_ficticio": usuario_ficticio.correo_usuario }), 200