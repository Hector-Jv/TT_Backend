from flask import Blueprint, jsonify, redirect, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario
from app.classes.validacion import Validacion
from app.classes.consulta import Consulta

favoritos_bp = Blueprint('sitios favoritos', __name__)

@favoritos_bp.route('/agregar_sitio_favorito', methods=["POST"])
@jwt_required()
def agregar_sitio_favorito():
    
    ## Datos necesarios ##
    # Token de usuario
    # json con la clave de sitio
    
    identificador_usuario = get_jwt_identity()
    usuario = Usuario.query.get(identificador_usuario)
    data = request.get_json()
    cve_sitio = data.get("cve_sitio")
    
    if not usuario:
        return jsonify({"error": "Necesitas estar logueado.", "id_usuario": identificador_usuario}), 404
    
    try:
        conexion_db = Consulta()
        conexion_db.cursor.callproc('agregar_quitar_sitio_favorito', [cve_sitio])
    finally:
        conexion_db.cerrar_conexion_db()
    return jsonify({"mensaje": "Añadido a favoritos."}), 200


@favoritos_bp.route('/mostrar_sitio_ur', methods=["GET"])
@jwt_required()
def mostrar_sitio_usuario_registrado():
    ## Datos necesarios ##
    # Token de usuario
    # json con la clave de sitio
    
    identificador_usuario = get_jwt_identity()
    usuario = Usuario.query.get(identificador_usuario)
    data = request.get_json()
    cve_sitio = data.get("cve_sitio")
    
    if not usuario:
        return jsonify({"error": "Necesitas estar logueado.", "id_usuario": identificador_usuario}), 404

    sitio = Consulta()
    datos_sitio = sitio.obtener_sitio(cve_sitio)

    try:
        conexion_db = Consulta()
        conexion_db.cursor.callproc('es_sitio_favorito', [cve_sitio, usuario.correo_usuario])
        resultados = conexion_db.cursor.stored_results()
        for resultado in resultados:
            dato_resultado = resultado.fetchone()
            datos_sitio["favorito"] = dato_resultado
    finally:
        conexion_db.cerrar_conexion_db()
        
        
    return jsonify(datos_sitio), 200
    
    
    
    
@favoritos_bp.route('/mostrar_sitios_favoritos', methods=["GET"])
@jwt_required()
def mostrar_sitios_favoritos():
    
    ## Se obtienen los datos ##
    identificador_usuario = get_jwt_identity()
    usuario = Usuario.query.get(identificador_usuario)
    
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