from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.classes.imagen import Imagen
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio, Etiqueta, Servicio, ServicioHotel, SitioEtiqueta, FotoSitio, Historial, Calificacion, CalificacionHotel, CalificacionRestaurante, Comentario, FotoComentario
from app.classes.validacion import Validacion
from app.classes.modificar_sitio import modificar_sitio
import json

eliminar_sitio_bp = Blueprint('Eliminar sitio', __name__)

@eliminar_sitio_bp.route('/eliminar_sitio', methods=['DELETE'])
def eliminar_sitio():
    
    ## Se piden los datos ##
    data = request.get_json()
    cve_sitio = data.get("cve_sitio")
    
    if not cve_sitio:
        return jsonify({"error": "Es necesario mandar la clave del sitio a eliminar."}), 400
    
    sitio_encontrado = Sitio.obtener_sitio_por_cve(cve_sitio)
    
    if sitio_encontrado is None:
        return jsonify({"error": "No existe el sitio a eliminar."}), 400
    
    ## Historial ##
    historiales_encontrados = Historial.obtener_historiales_por_sitio(cve_sitio)
    
    if historiales_encontrados:
        for historial in historiales_encontrados:
           
            ## Calificaciones ##
            calificaciones_encontradas = Calificacion.obtener_calificaciones_por_cvehistorial(historial.cve_historial)
           
            if calificaciones_encontradas:
                
                for calificacion in calificaciones_encontradas:
                    ## Calificacion especifica (hotel) ##
                    if TipoSitio.obtener_tipositio_por_nombre("Hotel").cve_tipo_sitio == sitio_encontrado.cve_tipo_sitio:
                        calificacionhotel_encontrada: CalificacionHotel = CalificacionHotel.obtener_calificacionhotel_por_cve(calificacion.cve_calificacion)
                        if calificacionhotel_encontrada:
                            CalificacionHotel.eliminar_calificacion(calificacionhotel_encontrada.cve_calificacion)
                    ## Calificacion especifica (hotel) ##
                    if TipoSitio.obtener_tipositio_por_nombre("Restaurante").cve_tipo_sitio == sitio_encontrado.cve_tipo_sitio:
                        calificacionrestaurante: CalificacionRestaurante = CalificacionRestaurante.obtener_calificacionrestaurante_por_cve(calificacion.cve_calificacion)
                        if calificacionrestaurante:
                            CalificacionRestaurante.eliminar_calificacion(calificacionrestaurante.cve_calificacion)
            
                    Calificacion.eliminar_calificacion(calificacion)
            
            ## Comentarios ##
            comentarios_encontrados = Comentario.obtener_comentario_por_historial(historial.cve_historial)
            
            if comentarios_encontrados:
                
                for comentario in comentarios_encontrados:
                    ## Foto comentario ##
                    fotos_encontradas = FotoComentario.obtener_fotos_por_comentario(comentario.cve_comentario)
                    
                    if fotos_encontradas:
                        for foto in fotos_encontradas:
                            FotoComentario.eliminar_foto(foto.cve_foto_comentario)
                    
                    Comentario.eliminar_comentario(comentario.cve_comentario)
            
            Historial.eliminar_historial(historial.cve_historial)    
              
    ## FotoSitio ##
    fotossitio_encontradas = FotoSitio.obtener_fotositio_por_cve(cve_sitio)
    
    if fotossitio_encontradas:
        for foto in fotossitio_encontradas:
            FotoSitio.eliminar_foto(foto.cve_foto_sitio)
    
    ## Horarios ##
    horarios_encontrados = Horario.obtener_horarios_por_sitio(cve_sitio)
    
    if horarios_encontrados:
        for horario in horarios_encontrados:
            Horario.eliminar_horario(horario.cve_horario)
    
    ## Si el sitio es un Hotel, eliminar sus relaciones con los servicios ##
    if TipoSitio.obtener_tipositio_por_cve(sitio_encontrado.cve_tipo_sitio).tipo_sitio == "Hotel":
        servicios_encontrados = ServicioHotel.obtener_relaciones_por_cvesitio(cve_sitio)
        
        if servicios_encontrados:
            ServicioHotel.eliminar_relaciones_por_cvesitio(cve_sitio)
    
    ## Si el sitio es un Restaurante o Museo, eliminar sus relaciones con las etiquetas ##
    if TipoSitio.obtener_tipositio_por_cve(sitio_encontrado.cve_tipo_sitio).tipo_sitio == "Restaurante" or TipoSitio.obtener_tipositio_por_cve(sitio_encontrado.cve_tipo_sitio).tipo_sitio == "Museo":
        etiquetas_encontradas = SitioEtiqueta.obtener_relaciones_por_cvesitio(cve_sitio)
        
        if etiquetas_encontradas:
            for relacion in etiquetas_encontradas:
                SitioEtiqueta.eliminar_relacion(cve_sitio=relacion.cve_sitio, cve_etiqueta=relacion.cve_etiqueta)
            
    Sitio.eliminar_sitio(cve_sitio)
    
    return jsonify({"mensaje": "Se ha eliminado el sitio correctamente."}), 201
