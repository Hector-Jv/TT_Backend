from flask import Blueprint, jsonify, redirect, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Usuario
from app.classes.consulta import Consulta

agregar_favorito_bp = Blueprint('Agregar sitio favorito', __name__)

@agregar_favorito_bp.route('/agregar_sitio_favorito', methods=["POST"])
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
        conexion_db.cursor.callproc('agregar_quitar_sitio_favorito', [cve_sitio, usuario.correo_usuario])
    finally:
        conexion_db.cerrar_conexion_db()
    return jsonify({"mensaje": "Añadido a favoritos."}), 200