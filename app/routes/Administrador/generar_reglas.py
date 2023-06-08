from flask import Blueprint, jsonify
from app.system_recomendations.apriori import Apriori
from itertools import groupby
from app.models import Historial
import json

generar_reglas_bp = Blueprint('Generar reglas asociacion', __name__)

@generar_reglas_bp.route('/generar_reglas', methods=['POST'])
def generar_reglas():
    
    soporte_minimo = 2
    confianza = 0.70 # Se refiere al porcentaje
    
    ## Se hace una conexion a la base de datos para obtener el historial ##
    historiales_encontrados = Historial.query.all()
    arreglo_historiales = [(historial.correo_usuario, historial.cve_sitio) for historial in historiales_encontrados]
    
    # Se ordena por correo electronico
    arreglo_historiales.sort(key=lambda x: x[0])
    
    # Se agrupan por correo electrónico
    historial_usuarios = [list(map(lambda x: x[1], grupo)) for clave, grupo in groupby(arreglo_historiales, lambda x: x[0])]
    
    """
    datos = [
        [1,2,3], # 1
        [2,4], # 2
        [5,2], # 3
        [2,3,4], # 4
        [5,3], # 5
        [5,2], # 6
        [5,3], # 7
        [5,2,3], # 8
        [1,2,3,5] # 9
    ]
    1 algodon
    2 cubrebocas
    3 gel
    4 guantes
    5 alcohol
    sistema_recomendacion = Apriori(datos, soporte_minimo)
    """
    
    
    sistema_recomendacion = Apriori(historial_usuarios, soporte_minimo, confianza)
    reglas = sistema_recomendacion.iniciar_algoritmo()
    
    with open('app/data/reglas_asociacion.json', 'w') as f:
        json.dump(reglas, f)
    return jsonify({"mensaje": "Se han generado las reglas de asociación con exito."}), 200