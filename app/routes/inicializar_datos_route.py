from flask import Blueprint, jsonify, request
from app import db
from app.models import *

inicial_bp = Blueprint('inicializar', __name__)

@inicial_bp.route('/inicializar', methods=['GET'])
def inicializar_datos_bd():
    
    if TipoUsuario.obtener_id_tipo_usuario("Usuario registrado") is not None:
        return jsonify({"mensaje": "Los datos ya existen."}), 400
    
    TipoUsuario.agregar_tipo_usuario("Usuario registrado")
    TipoUsuario.agregar_tipo_usuario("Administrador")
    TipoUsuario.agregar_tipo_usuario("Usuario eliminado")
    
    TipoSitio.agregar_tipo_sitio("Museo")
    TipoSitio.agregar_tipo_sitio("Teatro")
    TipoSitio.agregar_tipo_sitio("Monumento")
    TipoSitio.agregar_tipo_sitio("Parque")
    TipoSitio.agregar_tipo_sitio("Hotel")
    TipoSitio.agregar_tipo_sitio("Restaurante")
    
    Delegacion.agregar_delegacion("Álvaro Obregón")
    Delegacion.agregar_delegacion("Benito Juárez")
    Delegacion.agregar_delegacion("Azcapotzalco")
    Delegacion.agregar_delegacion("Coyoacán")
    Delegacion.agregar_delegacion("Cuajimalpa de Morelos")
    Delegacion.agregar_delegacion("Cuauhtémoc")
    Delegacion.agregar_delegacion("Gustavo A. Madero")
    Delegacion.agregar_delegacion("Iztacalco")
    Delegacion.agregar_delegacion("Iztapalapa")
    Delegacion.agregar_delegacion("Magdalena Contreras")
    Delegacion.agregar_delegacion("Miguel Hidalgo")
    Delegacion.agregar_delegacion("Milpa Alta")
    Delegacion.agregar_delegacion("Tláhuac")
    Delegacion.agregar_delegacion("Tlalpan")
    Delegacion.agregar_delegacion("Venustiano Carranza")
    Delegacion.agregar_delegacion("Xochimilco")
    
    return jsonify({"mensaje": "Datos inicializados."}), 200
    
    
    
    