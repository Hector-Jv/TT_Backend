from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Usuario, Historial
from app.classes.consulta import Consulta

mostrar_sitio_bp = Blueprint('Mostrar sitio', __name__)

@mostrar_sitio_bp.route('/mostrar_sitio_ur', methods=["GET"])
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
    
    Historial.agregar_historial(usuario.correo_usuario, cve_sitio)

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