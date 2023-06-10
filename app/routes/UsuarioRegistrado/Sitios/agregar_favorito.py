from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, SitioFavorito

agregar_favorito_bp = Blueprint('agregar_favorito', __name__)

@agregar_favorito_bp.route('/agregar_sitio_favorito', methods=["POST"])
def agregar_sitio_favorito():
    
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
        
    sitiofavorito_encontrado: SitioFavorito = SitioFavorito.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario, cve_sitio=cve_sitio).first()
    if not sitiofavorito_encontrado:
        nueva_relacion = SitioFavorito(
            cve_sitio,
            usuario_encontrado.correo_usuario
            
        )
        db.session.add(nueva_relacion)
        db.session.commit()
        return jsonify({"mensaje": "Añadido a favoritos."}), 200
        
    try:
        if sitiofavorito_encontrado.me_gusta:
            sitiofavorito_encontrado.me_gusta = False
            db.session.commit()
            return jsonify({"mensaje": "Quitado de favoritos."}), 200
        else:
            sitiofavorito_encontrado.me_gusta = True
            db.session.commit()
            return jsonify({"mensaje": "Añadido a favoritos."}), 200
    except Exception as e:
        db.session.callback()
        return jsonify({"error": "Hubo un error al agregar/quitar de favoritos"}), 400
        