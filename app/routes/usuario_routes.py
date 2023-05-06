from flask import jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Usuario, TipoUsuario, Historial, Preferencia

usuario_bp = Blueprint('usuario registrado', __name__)


@usuario_bp.route('/usuario', methods=['GET'])
@jwt_required()
def obtener_usuario():
    
    # Se obtiene la identidad del usario del token.
    identificador_usuario = get_jwt_identity()

    # Se obtiene el usuario que coincida con el token en la base de datos.
    usuario = Usuario.query.get(identificador_usuario)

    # Se verifica que exista el usuario en la base de datos.
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    
    # Se obtiene el tipo de usuario que pertenece el usuario.
    tipo_usuario = TipoUsuario.query.filter_by(cve_tipo_usuario=usuario.cve_tipo_usuario).first() 

    # Se obtiene el historial del usuario
    historial = Historial.query.filter_by(cve_usuario=usuario.correo_usuario).all()

    # Se obtienen las preferencias del usuario
    preferencias = Preferencia.query.filter_by(correo_usuario=usuario.correo_usuario).all()

    # Se devuelven los datos obtenidos del usuario.
    return jsonify({
        "usuario": {
            "usuario": usuario.usuario,
            "correo": usuario.correo_usuario,
            "foto_usuario": usuario.foto_usuario,
            "tipo_usuario": tipo_usuario.tipo_usuario,
        },
        "historial": [h.to_dict() for h in historial],
        "preferencias": [p.to_dict() for p in preferencias],
    }), 200
    
