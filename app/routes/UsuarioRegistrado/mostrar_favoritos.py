from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario
from app.classes.validacion import Validacion
from app.classes.consulta import Consulta

mostrar_sitios_favoritos_bp = Blueprint('mostrar_sitios_favoritos', __name__)

@mostrar_sitios_favoritos_bp.route('/mostrar_sitios_favoritos', methods=["GET"])
@jwt_required()
def mostrar_sitios_favoritos():
    
    identificador_usuario = get_jwt_identity()
    usuario: Usuario = Usuario.query.get(identificador_usuario)
    
    lista_sitios_encontrados = Historial.obtener_historiales_por_megusta(usuario.correo_usuario)
    
    lista_sitios_dict = []
    
    for sitio in lista_sitios_encontrados:
        tipo_sitio_encontrado = TipoSitio.obtener_tipositio_por_cve(sitio.cve_tipo_sitio)
        colonia_encontrada = Colonia.obtener_colonia_por_cve(sitio.cve_colonia)
        delegacion_encontrada = Delegacion.obtener_delegacion_por_cve(colonia_encontrada.cve_delegacion)
        fotositio_encontrada = FotoSitio.obtener_fotositio_por_cve(sitio.cve_sitio)
        
        historiales = Historial.obtener_historiales_por_sitio(sitio.cve_sitio)
        
        ## Se obtiene el número de visitas ##
        visitas = len(historiales)
        
        ## Se obtiene la calificacion promedio de cada sitio ##
        suma = 0
        num_calificaciones = 0
        promedio = None
        for historial in historiales:
            calificacion_encontrada = Calificacion.obtener_calificacion_por_historial(historial.cve_historial)
            if Validacion.valor_nulo(calificacion_encontrada):
                continue
            else:
                suma += calificacion_encontrada.calificacion_general
                num_calificaciones += 1
        
        if not num_calificaciones == 0:
            promedio = suma / num_calificaciones
        
        sitio_dict = sitio.to_dict()
        sitio_dict["tipo_sitio"] = tipo_sitio_encontrado.tipo_sitio
        sitio_dict["colonia"] = colonia_encontrada.nombre_colonia
        sitio_dict["delegacion"] = delegacion_encontrada.nombre_delegacion
        sitio_dict["num_visitas"] = visitas
        sitio_dict["calificacion"] = promedio
        sitio_dict["foto"] = None
        if fotositio_encontrada is not None:
            sitio_dict["foto"] = [foto.nombre_imagen for foto in fotositio_encontrada]
        
        lista_sitios_dict.append(sitio_dict)
        
    return jsonify(lista_sitios_dict), 200

