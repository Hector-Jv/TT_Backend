from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Usuario,TipoUsuario, ServicioHotel, SitioEtiqueta, FotoSitio, Historial, Comentario, FotoComentario, SitioFavorito

eliminar_sitio_bp = Blueprint('eliminar_sitio', __name__)

@eliminar_sitio_bp.route('/eliminar_sitio', methods=['DELETE'])
def eliminar_sitio():
    
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
        return jsonify({"error": "El usuario no es administrador. No puede borrar el sitio."}), 403
        
    ## VALIDACIÓN DE SITIO ##
    
    sitio_encontrado: Sitio = Sitio.query.get(cve_sitio)
    if sitio_encontrado is None:
        return jsonify({"error": "No existe el sitio a eliminar."}), 400
    
    ## ELIMINACIÓN DE SITIO ##
    try:
        historiales_encontrados = Historial.query.filter_by(cve_sitio = cve_sitio).all()
        if historiales_encontrados:
            for historial in historiales_encontrados:
                ## Comentarios ##
                comentarios_encontrados = Comentario.query.filter_by(cve_historial = historial.cve_historial).all()
                if comentarios_encontrados:
                    for comentario in comentarios_encontrados:
                        ## Foto comentario ##
                        fotos_encontradas = FotoComentario.query.filter_by(cve_comentario = comentario.cve_comentario).all()
                        if fotos_encontradas:
                            for foto in fotos_encontradas:
                                db.session.delete(foto)
                        db.session.delete(comentario)
                db.session.delete(historial)  
                
        ## FotoSitio ##
        fotossitio_encontradas = FotoSitio.query.filter_by(cve_sitio = cve_sitio)
        if fotossitio_encontradas:
            for foto in fotossitio_encontradas:
                db.session.delete(foto)
        
        ## Etiquetas ##
        etiquetas_encontradas = SitioEtiqueta.query.filter_by(cve_sitio = cve_sitio).all()
        if etiquetas_encontradas:
            for etiqueta in etiquetas_encontradas:
                db.session.delete(etiqueta)
        
        ## Servicios ##
        servicios_encontrados = ServicioHotel.query.filter_by(cve_sitio = cve_sitio).all()
        if servicios_encontrados:
            for servicio in servicios_encontrados:
                db.session.delete(servicio)
                
        ## SitioFavorito ##
        sitios_favoritos = SitioFavorito.query.filter_by(cve_sitio = cve_sitio).all()
        if sitios_favoritos:
            for sitio in sitios_favoritos:
                db.session.delete(sitio)
        
        db.session.delete(sitio_encontrado)
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Se produjo un error al querer eliminar el sitio.", "error": str(e)}), 400
    db.session.commit()
    return jsonify({"mensaje": "Se ha eliminado el sitio correctamente."}), 200
