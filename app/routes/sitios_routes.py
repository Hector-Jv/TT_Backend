from flask import Blueprint, jsonify, redirect, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario

sitio_bp = Blueprint('sitio', __name__)

"""
Rutas creadas:
    /inicio [GET]
    /sitios [GET]
    /sitios/filtros [GET]
    /sitios/<nombre sitio> [GET]
"""
@sitio_bp.route('/')
def menu():
    return redirect("/inicio")


@sitio_bp.route('/inicio', methods=["GET"])
def mostrar_tipo_sitios():
    
    lista_tipo_sitios, codigo = TipoSitio.consultar_todos()
    
    return jsonify({"tipo_sitios": lista_tipo_sitios}), codigo

@sitio_bp.route('/sitios', methods=["GET"])
def mostrar_sitios():
    
    data = request.get_json()
    
    tipo_sitio = data.get("cve_tipo_sitio")
    opcion_ordenamiento = request.get("ordenamiento", default=1)

    
    lista_tipo_sitios, codigo = TipoSitio.consultar_todos()
    if codigo == 404:
        return jsonify({"Mensaje": "No se encontraron los tipos de sitios."}), 404

    lista_delegaciones, codigo = Delegacion.mostrar_todos()
    if codigo == 404:
        return jsonify({"Mensaje": "No se encontraron las delegaciones."}), 404
    
    lista_sitios, codigo = Sitio.consultar_sitios_por_tipo(tipo_sitio)
    nombre_tipo_sitio = TipoSitio.consultar_por_cve(tipo_sitio)
    if codigo == 404:
        return jsonify({"Mensaje": f"No se encontraron sitios de tipo {nombre_tipo_sitio[0]['tipo_sitio']}."}), 404
    
    for sitio in lista_sitios:
        colonia_sitio = Colonia.obtener_colonia_por_id(sitio["cve_colonia"])
        sitio["delegacion"] = Delegacion.buscar_por_cve(colonia_sitio.to_dict()["cve_delegacion"])[0]["nombre_delegacion"]
        sitio["colonia"] = colonia_sitio.to_dict()["nombre_colonia"]
    
    # Ordenar los datos.
    if opcion_ordenamiento == 1: # Ordenamiento por calificacion (por defecto)
        sitios_ordenados = sorted(lista_sitios, key=lambda sitio: sitio.calificacion_general, reverse=True)
    elif opcion_ordenamiento == 2: # Ordenamiento por número de visitas
        sitios_ordenados = sorted(lista_sitios, key=lambda sitio: len(sitio.historiales), reverse=True)
    elif opcion_ordenamiento == 3: # Ordenamiento por mayor costo
        sitios_ordenados = sorted(lista_sitios, key=lambda sitio: sitio.costo_promedio or float('inf'), reverse=True)
    elif opcion_ordenamiento == 4: # Ordenamiento por menor costo
        sitios_ordenados = sorted(lista_sitios, key=lambda sitio: sitio.costo_promedio or 0)
    else:
        return jsonify({"error": "No existe el ordenamiento especificado."}), 400

    sitios_ordenados_json = [sitio.to_dict() for sitio in sitios_ordenados]

    return jsonify({
        "tipo_sitios": lista_tipo_sitios,
        "delegaciones": lista_delegaciones,
        "sitios": sitios_ordenados_json}), 200
    

@sitio_bp.route('/sitios/filtros', methods=["GET"])
def mostrar_sitios_con_filtros():
    
    data = request.get_json()
    
    cve_tipo_sitio = request.get("cve_tipo_sitio")
    precio_min = request.get("precio_min", default=0, type=int)
    precio_max = request.get("precio_max", default=float('inf'), type=int)
    calificacion_min = request.get("calificacion", default=0, type=float)
    cve_delegacion = request.get("cve_delegacion")
    opcion_ordenamiento = request.get("ordenamiento", default=1)
    """
    Opciones de ordenamiento:
        1. Mejor calificados (Por defecto).
        2. Mas visitados.
        3. Mayor precio.
        4. Menor precio.
    """
    
    if cve_tipo_sitio is None:
        return jsonify({"Error": "Se debe especificar el tipo de sitio a buscar."}), 400

    sitios_por_tipo_sitio = Sitio.consultar_sitios_por_tipo(cve_tipo_sitio)[0]
    
    # Aplicando los filtros
    sitios_filtrados = []
    for sitio in sitios_por_tipo_sitio:
        if sitio["costo_promedio"] is None or precio_min <= sitio["costo_promedio"] <= precio_max:
            
            union_calificacion_historial = Calificacion.query.join(Historial)
            filtered_query = union_calificacion_historial.filter(Historial.cve_sitio == sitio["cve_sitio"])
            calificaciones_sitio = [calificacion.calificacion_general for calificacion in filtered_query.all()]
            
            if calificaciones_sitio:
                promedio_calificaciones = sum(calificaciones_sitio) / len(calificaciones_sitio)
            else:
                promedio_calificaciones = None  # o cualquier valor por defecto que desees asignar
            
            if (promedio_calificaciones is None or promedio_calificaciones >= calificacion_min) and (cve_delegacion is None or sitio["cve_delegacion"] == cve_delegacion):
                sitios_filtrados.append(sitio)
    
    # Ordenar los datos.
    if opcion_ordenamiento == 1: # Ordenamiento por calificacion (por defecto)
        sitios_ordenados = sorted(sitios_filtrados, key=lambda sitio: sitio.calificacion_general, reverse=True)
    elif opcion_ordenamiento == 2: # Ordenamiento por número de visitas
        sitios_ordenados = sorted(sitios_filtrados, key=lambda sitio: len(sitio.historiales), reverse=True)
    elif opcion_ordenamiento == 3: # Ordenamiento por mayor costo
        sitios_ordenados = sorted(sitios_filtrados, key=lambda sitio: sitio.costo_promedio or float('inf'), reverse=True)
    elif opcion_ordenamiento == 4: # Ordenamiento por menor costo
        sitios_ordenados = sorted(sitios_filtrados, key=lambda sitio: sitio.costo_promedio or 0)
    else:
        return jsonify({"error": "No existe el ordenamiento especificado."}), 400

    sitios_ordenados_json = [sitio.to_dict() for sitio in sitios_ordenados]

    return jsonify({"Sitios": sitios_ordenados_json}), 200


@sitio_bp.route('/sitios/<cve_sitio>', methods=["GET"])
def mostrar_info_sitio(cve_sitio):
    
    info_sitio = Sitio.consultar_sitio(cve_sitio)
    
    info_sitio[0]["imagenes"] = FotoSitio.obtener_fotos_por_sitio(cve_sitio)[0]
    info_sitio[0]["horarios"] = list(Horario.consultar_horarios_por_sitio(cve_sitio))[0]
    colonia_sitio = Colonia.obtener_colonia_por_id(info_sitio[0]["cve_colonia"])
    info_sitio[0]["delegacion"] = Delegacion.buscar_por_cve(colonia_sitio.to_dict()["cve_delegacion"])[0]["nombre_delegacion"]
    info_sitio[0]["colonia"] = colonia_sitio.to_dict()["nombre_colonia"]
    
    historiales = Historial.consultar_historiales_por_sitio(cve_sitio)
    if historiales[0] is not None:
        acumulador = 0
        contador_none = 0
        for historial in historiales[0]:
            calificacion, codigo = Calificacion.consultar_calificacion(historial["cve_historial"])
            if codigo == 200:
                acumulador += calificacion
            else:
                contador_none +=1
        info_sitio[0]["promedio"] = acumulador / (len(historiales) - contador_none)
    
    info_sitio[0]["tipo_sitio"] = TipoSitio.consultar_por_cve(info_sitio[0]["cve_tipo_sitio"])[0]["tipo_sitio"]
    
    if info_sitio[0]["tipo_sitio"] == "Hotel":
        relaciones = ServicioHotel.consultar_por_cve_sitio(cve_sitio)[0]
        if relaciones is not None:
            servicios = []
            for relacion in relaciones:
                servicio = Servicio.consultar_por_cve(relacion["cve_servicio"])[0]
                servicios.append(servicio["nombre_servicio"])
            info_sitio[0]["servicios"] = servicios
            
    if info_sitio[0]["tipo_sitio"] == "Museo" or info_sitio[0]["tipo_sitio"] == "Restaurante":
        relaciones = SitioEtiqueta.consultar_relaciones_por_sitio(cve_sitio)[0]
        if relaciones is not None:
            etiquetas = []
            for relacion in relaciones:
                etiqueta = Etiqueta.consultar_etiqueta_por_cve(relaciones["cve_etiqueta"])[0]
                etiquetas.append(etiqueta["nombre_etiqueta"])
            info_sitio[0]["etiquetas"] = etiquetas
    
    return jsonify({"sitio": info_sitio[0]}), 200

## PENDIENTE
@sitio_bp.route('/sitio_favorito', methods=["POST"])
@jwt_required()
def sitio_favorito():
    
    identificador_usuario = get_jwt_identity()
    usuario = Usuario.query.get(identificador_usuario)

    if not usuario:
        return jsonify({"error": "Necesitas estar logueado.", "id_usuario": identificador_usuario}), 404
    
    return jsonify({"usuario": usuario}), 200
