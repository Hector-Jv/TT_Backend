from flask import Blueprint, jsonify, redirect, request
#from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario
from app.classes.consulta import Consulta

sitios_bp = Blueprint('consulta sitios', __name__)

@sitios_bp.route('/mostrar_sitios', methods=["GET"])
def mostrar_sitios():
    
    ## Se obtienen los datos ##
    data = request.get_json()
    cve_tipo_sitio = data.get("cve_tipo_sitio")
    ordenamiento = data.get("ordenamiento")
    pagina = data.get("pagina")
    """
    precio_min = data.get("precio_min")
    precio_max = data.get("precio_max") 
    calificacion_min = data.get("calificacion_min") 
    cve_delegacion = data.get("cve_delegacion")
    
    , precio_min, precio_max, calificacion_min, cve_delegacion
    """
    
    conexion_db = Consulta()
    sitios_encontrados, num_sitios = conexion_db.obtener_sitios(cve_tipo_sitio, ordenamiento, pagina)
    conexion_db.cerrar_conexion_db()
    
    return jsonify(sitios_encontrados, num_sitios), 200


@sitios_bp.route('/mostrar_sitio', methods=["GET"])
def mostrar_info_sitio():
    
    data = request.get_json()
    cve_sitio = data.get("cve_sitio")
    
    info_sitio: dict = {}
    
    sitio_encontrado: Sitio = Sitio.obtener_sitio_por_cve(cve_sitio)
    colonia_encontrada: Colonia = Colonia.obtener_colonia_por_cve(sitio_encontrado.cve_colonia)
    delegacion_encontrada: Delegacion = Delegacion.obtener_delegacion_por_cve(colonia_encontrada.cve_delegacion)
    fotossitio_encontrado: list = FotoSitio.obtener_fotositio_por_cve(cve_sitio)
    horarios_encontrados: list = Horario.obtener_horarios_por_sitio(cve_sitio)
    tipositio_encontrado: TipoSitio = TipoSitio.obtener_tipositio_por_cve(sitio_encontrado.cve_tipo_sitio)
    
    servicioshotel_encontrados = None
    sitioetiqueta_encontrados = None
    if tipositio_encontrado.tipo_sitio == 'Hotel':
        servicioshotel_encontrados: list = ServicioHotel.obtener_relaciones_por_cvesitio(cve_sitio)
    if tipositio_encontrado.tipo_sitio == 'Museo' or tipositio_encontrado.tipo_sitio == 'Hotel':
        sitioetiqueta_encontrados: list = SitioEtiqueta.obtener_relaciones_por_cvesitio(cve_sitio)
    
    # Calificación de sitio
    historiales_encontrados = Historial.obtener_historiales_por_sitio(cve_sitio)
    sum = 0
    num_elementos = 0
    visitas = 0
    calificacion_sitio = 0
    if historiales_encontrados:
        for historial in historiales_encontrados:
            visitas += 1
            calificacion_encontrada: Calificacion = Calificacion.obtener_calificacion_por_historial(historial.cve_historial)
            if calificacion_encontrada is None:
                continue
            sum += calificacion_encontrada.calificacion_general
            num_elementos += 1
        calificacion_sitio = sum / num_elementos
    
    ## Se pasan a diccionarios ##
    sitio_encontrado_dict: dict = sitio_encontrado.to_dict()
    colonia_encontrada_dict: dict = colonia_encontrada.to_dict()
    delegacion_encontrada_dict: dict = delegacion_encontrada.to_dict()
    if fotossitio_encontrado:
        lista_fotositio = [foto.to_dict() for foto in fotossitio_encontrado]
    else:
        lista_fotositio = []
    if horarios_encontrados:
        lista_horarios = [horario.to_dict() for horario in horarios_encontrados]
    else:
        lista_horarios = []
    tipositio_encontrado_dict: dict = tipositio_encontrado.to_dict()
    if servicioshotel_encontrados is not None:
        info_sitio["servicioshotel_encontrados"] = [servicio.to_dict() for servicio in servicioshotel_encontrados]
    if sitioetiqueta_encontrados is not None:
        info_sitio["sitioetiqueta_encontrados"] = [relacion for relacion in sitioetiqueta_encontrados]
    
    
    info_sitio = sitio_encontrado_dict | colonia_encontrada_dict | delegacion_encontrada_dict | tipositio_encontrado_dict
    info_sitio["lista_fotositio"] = lista_fotositio
    info_sitio["lista_horarios"] = lista_horarios
    info_sitio["visitas"] = visitas
    info_sitio["calificacion"] = calificacion_sitio
    
    return jsonify(info_sitio), 200
