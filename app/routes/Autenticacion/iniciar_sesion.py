from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, TipoUsuario, UsuarioServicio, UsuarioEtiqueta

iniciar_sesion_bp = Blueprint('iniciar_sesion', __name__)

@iniciar_sesion_bp.route('/login', methods=['POST'])
def inicio_sesion():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ['correo_usuario', 'contrasena']
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "JSON malformado."}), 400
    
    for id in identificadores:
        if id not in request.get_json():
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    correo_usuario: str = data.get('correo_usuario')
    contrasena: str = data.get('contrasena')
    
    if not correo_usuario or not isinstance(correo_usuario, str):
        return jsonify({"error": "Es necesario mandar un valor valido en correo_usuario."}), 400
    
    if not contrasena or not isinstance(contrasena, str):
        return jsonify({"error": "Es necesario mandar un valor valido en contrasena."}), 400
    
    ## VALIDACIÓN DE PERMISOS ##

    usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
    if not usuario_encontrado:
        return jsonify({"error": "El correo no se encuentra registrado."}), 404
    if not usuario_encontrado.verificar_contrasena(contrasena):
        return jsonify({"error": "Contraseña incorrecta"}), 401
    
    ## SE REGRESAN LOS DATOS DEL USUARIO REGISTRADO ##
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    
    return jsonify({
        "correo_usuario": usuario_encontrado.correo_usuario,
        "usuario": usuario_encontrado.usuario,
        "cve_tipo_usuario": usuario_encontrado.cve_tipo_usuario,
        "tipo_usuario": tipo_usuario.tipo_usuario,
        "link_imagen": usuario_encontrado.link_imagen,
        "servicios": [servicio.cve_servicio for servicio in UsuarioServicio.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario).all()],
        "etiquetas": [etiqueta.cve_etiqueta for etiqueta in UsuarioEtiqueta.query.filter_by(correo_usuario=usuario_encontrado.correo_usuario).all()]
    }), 200

        