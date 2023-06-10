from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Usuario, TipoUsuario

inhabilitar_sitio_bp = Blueprint('inhabilitar_sitio', __name__)

@inhabilitar_sitio_bp.route('/inhabilitar_sitio', methods=['PUT'])
def inhabilitar_sitio():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ["correo_usuario", "cve_sitio"]
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400


    correo_usuario = data.get("correo_usuario")
    cve_sitio = data.get("cve_sitio")
    
    if not cve_sitio or not isinstance(cve_sitio, int):
        return jsonify({"error": "Es necesario mandar un valor valido en cve_sitio."}), 400
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    ## VALIDACIÓN DE PERMISOS ##
    
    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "Es necesario ingresar con un correo registrado."}), 400
        
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    if tipo_usuario.tipo_usuario != 'Administrador':
        return jsonify({"error": "El usuario no es administrador. No puede inhabilitar el sitio."}), 403
        
    ## VALIDACIÓN DE SITIO ##
    
    sitio_encontrado: Sitio = Sitio.query.get(cve_sitio)
    if sitio_encontrado is None:
        return jsonify({"error": "No existe el sitio a eliminar."}), 400
    
    ## INHABILITAR SITIO ##
    
    try:
        if sitio_encontrado.habilitado == True:
            sitio_encontrado.habilitado = False
        else:
            sitio_encontrado.habilitado = True
    except Exception as e:
        return jsonify({"error": "Hubo un error."}), 400
    db.session.commit()
    return jsonify({"mensaje": "Se han realizado los cambios."}), 200
    