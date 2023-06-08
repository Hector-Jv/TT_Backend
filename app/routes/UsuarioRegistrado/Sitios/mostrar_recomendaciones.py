from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Historial, Usuario
import json

mostrar_recomendaciones_bp = Blueprint('Mostrar recomendaciones', __name__)

#@jwt_required()
@mostrar_recomendaciones_bp.route('/mostrar_recomendaciones', methods=["GET"])
def mostrar_sitios_favoritos():
    
    # Datos necesarios ##
    # Token de usuario
    # json con la clave de sitio
    #print("Usuario: ", usuario_encontrado.correo_usuario)
    
    # identificador_usuario = get_jwt_identity()
    #usuario_encontrado:Usuario = Usuario.query.get(identificador_usuario)
    nom_usuario = 'Aaron'
    usuario_encontrado:Usuario = Usuario.query.filter_by(usuario=nom_usuario)
    
    print("Usuario: ", usuario_encontrado.correo_usuario)
    
    historiales_encontrados = Historial.query.filter_by(cve_usuario = usuario_encontrado.correo_usuario).all()
    historiales_de_usuario = sorted([historial.cve_sitio for historial in historiales_encontrados])
    
    if len(historiales_de_usuario) < 2:
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

