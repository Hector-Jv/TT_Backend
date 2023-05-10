from flask import jsonify, Blueprint, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Usuario, TipoUsuario, Historial, Preferencia, Sitio, TipoSitio, Colonia, Delegacion

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
    
    if tipo_usuario.tipo == 'Administrador':
        return redirect(url_for('menu_administrador'))


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
    
    
@usuario_bp.route('/admin', methods=['GET'])
@jwt_required()
def menu_administrador():
    
    # Se obtienen todos los sitios registrados.
    sitios = Sitio.query.all()
    
    lista_sitios = []
    
    for sitio in sitios:
        info_sitio = {}
        info_sitio["cve_sitio"] = sitio.cve_sitio
        info_sitio["nombre_sitio"] = sitio.nombre_sitio
        info_sitio["x_longitud"] = sitio.x_longitud
        info_sitio["y_latitud"] = sitio.y_latitud
        info_sitio["direccion"] = sitio.direccion
        info_sitio["fecha_actualizacion"] = sitio.fecha_actualizacion
        info_sitio["descripcion"] = sitio.descripcion
        info_sitio["correo_sitio"] = sitio.correo_sitio
        info_sitio["fecha_fundacion"] = sitio.fecha_fundacion
        info_sitio["costo_promedio"] = sitio.costo_promedio
        info_sitio["habilitado"] = sitio.habilitado
        info_sitio["pagina_web"] = sitio.pagina_web
        info_sitio["telefono"] = sitio.telefono
        info_sitio["adscripcion"] = sitio.adscripcion
        
        # Busca el tipo de sitio que pertenece.
        tipo_sitio_objeto = TipoSitio.query.filter_by(cve_tipo_sitio=sitio.cve_tipo_sitio).first()
        
        info_sitio["tipo_sitio"] = tipo_sitio_objeto.tipo_sitio
        info_sitio["habilitado"] = sitio.habilitado
        
        # Busca la colonia al que pertenece.
        colonia_objeto = Colonia.query.filter_by(cve_colonia=sitio.cve_colonia).first()
        
        # Busca la delegacion al que pertenece.
        delegacion_objeto = Delegacion.query.filter_by(cve_delegacion=colonia_objeto.cve_delegacion).first()
        
        info_sitio["colonia"] = colonia_objeto.nombre_colonia
        info_sitio["delegacion"] = delegacion_objeto.nombre_delegacion
        
        # Faltan las fotografías, horarios, etiquetas, servicios
        lista_sitios.append(info_sitio)
        
    return jsonify(lista_sitios), 200
