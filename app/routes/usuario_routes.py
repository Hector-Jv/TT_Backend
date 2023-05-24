from flask import jsonify, Blueprint, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Usuario, TipoUsuario, Historial, Preferencia, Sitio, TipoSitio, Colonia, Delegacion

usuario_bp = Blueprint('usuario registrado', __name__)


@usuario_bp.route('/usuario', methods=['GET'])
@jwt_required()
def obtener_usuario():
    
    identificador_usuario = get_jwt_identity()
    usuario = Usuario.query.get(identificador_usuario)

    # Se verifica que exista el usuario en la base de datos.
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    
    # Se obtiene el tipo de usuario que pertenece el usuario.
    tipousuario_encontrado = TipoUsuario.obtener_tipousuario_por_cve(usuario.cve_tipo_usuario)
    
    if tipousuario_encontrado.tipo_usuario == 'Administrador':
        return redirect(url_for('menu_administrador'))

    # Se obtiene el historial del usuario
    historiales = Historial.obtener_historiales_por_usuario(usuario.correo_usuario)

    # Se obtienen las preferencias del usuario
    preferencias = Preferencia.obtener_preferencias_por_correo(usuario.correo_usuario)

    dic = {}
    dic = dic.update(usuario)
    dic["historial"] = [historial.to_dict() for historial in historiales]
    dic["preferencias"] = [preferencia.to_dict() for preferencia in preferencias]

    # Se devuelven los datos obtenidos del usuario.
    return jsonify(dic), 200
     
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
