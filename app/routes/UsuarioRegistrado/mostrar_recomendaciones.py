from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario
import json

mostrar_recomendaciones_bp = Blueprint('Mostrar recomendaciones', __name__)

@mostrar_recomendaciones_bp.route('/mostrar_recomendaciones', methods=["GET"])
@jwt_required()
def mostrar_sitios_favoritos():
    
    # Datos necesarios ##
    # Token de usuario
    # json con la clave de sitio
    
    identificador_usuario = get_jwt_identity()
    usuario_encontrado:Usuario = Usuario.query.get(identificador_usuario)
    
    historiales_encontrados = Historial.query.filter_by(cve_usuario = usuario_encontrado.correo_usuario).all()
    historiales_de_usuario = sorted([historial.cve_sitio for historial in historiales_encontrados])
    
    if len(historiales_de_usuario) < 5:
        return jsonify({"mensaje": "No hay suficientes datos para generar recomendaciones."}), 400

    with open('app/data/reglas_asociacion.json', 'r') as f:
        reglas_asociacion = json.load(f)
            
    print("Historiales de usuario: ", historiales_de_usuario)
    
    
    sitios_recomendados = []
    for regla in reglas_asociacion:
        cumple = True
        for elemento in regla["antecedente"]:
            if not elemento in historiales_de_usuario:
                cumple = False
                break
        if cumple:
            sitios_recomendados.append(regla["consecuente"])
            
        
    
    return jsonify({"mensaje": "en construccion"}), 200

