from flask import Blueprint, jsonify, request
from app.models import Usuario

### servicio para mostrar los usuario nombre, correo, habiltado
### servicio para mostrar el usuario (pasa correo_usuario) : nombre, correo, habilitado, comentarios, calificaciones.


mostrar_usuarios_bp = Blueprint('mostrar_usuarios', __name__)

@mostrar_usuarios_bp.route('/mostrar_usuarios', methods=['GET'])
def mostrar_usuarios(cve_tipo_sitio):
    
    usuarios_encontrados = Usuario.query.all()
    
    usuarios_arr = []
    for usuario in usuarios_encontrados:
        
        if usuario.cve_tipo_usuario != 1:
            continue
        
        usuario_dict = {}
        usuario_dict["correo"] = usuario.correo_usuario
        usuario_dict["usuario"] = usuario.usuario
        usuario_dict["habilitado"] = usuario.habilitado
        
        usuarios_arr.append(usuario_dict)
        
    return jsonify(usuarios_arr), 200