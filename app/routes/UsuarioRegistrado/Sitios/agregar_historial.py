from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, Historial, Comentario, FotoSitio, Sitio, SitioEtiqueta, Etiqueta, Colonia, Delegacion, TipoSitio, FotoComentario

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
    
    
    sitio_dict = {}
    sitio_encontrado: Sitio = Sitio.query.get(cve_sitio)
    
    if not sitio_encontrado:
        return jsonify({"error": "No existe el sitio."}), 400
    
    sitio_dict["cve_sitio"] = cve_sitio
    sitio_dict["nombre_sitio"] = sitio_encontrado.nombre_sitio
    sitio_dict["longitud"] = sitio_encontrado.longitud
    sitio_dict["latitud"] = sitio_encontrado.latitud
    sitio_dict["descripcion"] = sitio_encontrado.descripcion
    sitio_dict["correo"] = sitio_encontrado.correo_sitio
    sitio_dict["costo"] = sitio_encontrado.costo_promedio
    sitio_dict["pagina_web"] = sitio_encontrado.pagina_web
    sitio_dict["telefono"] = sitio_encontrado.telefono
    sitio_dict["adscripcion"] = sitio_encontrado.adscripcion
    sitio_dict["num_calificaciones"] = sitio_encontrado.num_calificaciones
    sitio_dict["calificacion"] = sitio_encontrado.calificacion
    
    fotos = []
    fotos_encontradas = FotoSitio.query.filter_by(cve_sitio=cve_sitio).all()
    for foto in fotos_encontradas:
        info_foto = {}
        info_foto["cve_foto"] = foto.cve_foto_sitio
        info_foto["nombre_imagen"] = foto.nombre_imagen
        info_foto["link_imagen"] = foto.link_imagen
        info_foto["nombre_autor"] = foto.nombre_autor
        fotos.append(info_foto)
    sitio_dict["fotos"] = fotos
    
    etiquetas = []
    etiquetas_encontradas = SitioEtiqueta.query.filter_by(cve_sitio=cve_sitio).all()
    for etiqueta in etiquetas_encontradas:
        etiqueta_encontrada = Etiqueta.query.get(etiqueta.cve_etiqueta)
        info_etiqueta = {}
        info_etiqueta["cve_etiqueta"] = etiqueta_encontrada.cve_etiqueta
        info_etiqueta["nombre_etiqueta"] = etiqueta_encontrada.nombre_etiqueta
        etiquetas.append(info_etiqueta)
    sitio_dict["etiquetas"] = etiquetas
    
    colonia_encontrada: Colonia = Colonia.query.filter_by(cve_colonia=sitio_encontrado.cve_colonia).first()
    delegacion_encontrada: Delegacion = Delegacion.query.get(colonia_encontrada.cve_delegacion)
    tipositio_encontrado: TipoSitio = TipoSitio.query.get(sitio_encontrado.cve_tipo_sitio)
    sitio_dict["colonia"] = colonia_encontrada.nombre_colonia
    sitio_dict["delegacion"] = delegacion_encontrada.nombre_delegacion
    sitio_dict["tipo_sitio"] = tipositio_encontrado.tipo_sitio
    
    comentarios = []
    historiales_encontradas = Historial.query.filter_by(cve_sitio=cve_sitio).all()
    for historial in historiales_encontradas:
        comentario = {}
        comentario_encontrado: Comentario = Comentario.query.filter_by(cve_historial=historial.cve_historial).first()
        if comentario_encontrado:
            fotos_comentarios = FotoComentario.query.filter_by(cve_comentario=comentario_encontrado.cve_comentario).all()
            fotosC = []
            for fotoC in fotos_comentarios:
                info_fotoC = {}
                info_fotoC["cve_foto_comentario"] = fotoC.cve_foto_comentario
                info_fotoC["nombre_imagen"] = fotoC.nombre_imagen
                info_fotoC["link_imagen"] = fotoC.link_imagen
                info_fotoC["nombre_autor"] = fotoC.nombre_autor
                fotosC.append(info_fotoC)
            comentario["cve_comentario"] = comentario_encontrado.cve_comentario
            comentario["comentario"] = comentario_encontrado.comentario
            comentario["fecha_comentario"] = comentario_encontrado.fecha_comentario
            comentario["fotos_comentario"] = fotosC
            comentarios.append(comentario)
    sitio_dict["comentarios"] = comentarios
    
    historial_usuario: Historial = Historial.query.filter_by(correo_usuario=correo_usuario, cve_sitio=cve_sitio).first()
    sitio_dict["visitado"] = historial_usuario.visitado
    sitio_dict["fecha_visita"] = historial_usuario.fecha_visita
    
    return jsonify({"datos_sitio": sitio_dict, "cve_sitio": cve_sitio, "mensaje": mensaje}), 200
        