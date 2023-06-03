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
    
    with open('app/data/reglas_asociacion.json', 'r') as f:
        reglas_asociacion = json.load(f)
        
    historiales_encontrados = Historial.query.filter_by(cve_usuario = usuario_encontrado.correo_usuario).all()
    historiales_de_usuario = [historial.cve_sitio for historial in historiales_encontrados]
    
    # for regla in reglas_asociacion:
        
    
    return jsonify({"mensaje": "en construccion"}), 200

