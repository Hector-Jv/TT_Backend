from flask import Blueprint, jsonify, request
from app.models import Sitio, Usuario, TipoSitio, FotoSitio, Colonia, Delegacion, SitioEtiqueta, Etiqueta, Historial, Comentario, FotoComentario
from app import db
from datetime import datetime

mostrar_sitio_bp = Blueprint('mostrar_sitio', __name__)

@mostrar_sitio_bp.route('/mostrar_sitio/<int:cve_sitio>', methods=["GET"])
def mostrar_info_sitio(cve_sitio):
    
    sitio_dict = {}
    
    correo_usuario = request.args.get('correo_usuario')
    if correo_usuario:
        usuario_encontrado: Usuario = Usuario.query.get(correo_usuario)
        if not usuario_encontrado:
            return jsonify({"error": "No se encontró un usuario registrado con ese correo."}), 400
        
        historial_encontrado: Historial = Historial.query.filter_by(
            correo_usuario=correo_usuario, 
            cve_sitio=cve_sitio
            ).first()
        
        if historial_encontrado:
            historial_encontrado.fecha_visita = datetime.utcnow()
        else:
            nuevo_historial = Historial(
                correo_usuario,
                cve_sitio
                )
            db.session.add(nuevo_historial)
            historial_encontrado = nuevo_historial
        db.session.commit()
        sitio_dict["visitado"] = historial_encontrado.visitado
    
    
    
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
    
    
    return jsonify(sitio_dict), 200
