from flask import Blueprint, jsonify, redirect, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.classes.consulta import Consulta

mostrar_sitio_bp = Blueprint('mostrar_sitio', __name__)

@mostrar_sitio_bp.route('/mostrar_sitio/<int: cve_sitio>', methods=["GET", "POST"])
def mostrar_info_sitio(cve_sitio):
    
    data = request.get_json()
    
    conexion_bd = Consulta()
    datos_sitio = conexion_bd.obtener_sitio(cve_sitio)
    conexion_bd.cerrar_conexion_db()
    
    return jsonify(datos_sitio), 200