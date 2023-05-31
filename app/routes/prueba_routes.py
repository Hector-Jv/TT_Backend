from flask import Blueprint, jsonify, request
from app import db
from app.classes.sistema_recomendacion import sistema_recomendacion

prueba_bp = Blueprint('Pruebas', __name__)

@prueba_bp.route('/pruebas', methods=['GET'])
def prueba_sistema_recomendacion():
    
    opinion_1 = "2, 1, 6, 7, 8"
    opinion_2 = "2, 1, 6, 7, 8"
    opinion_3 = "2, 1, 4, 9, 6, 7, 8"
    opinion_4 = "2, 1, 10, 9, 11, 7, 8"
    opinion_5 = "2, 1, 6, 7, 12, 13, 15, 16, 8"
    opinion_6 = "2, 1, 8"
    opinion_7 = "2, 1, 6, 7, 8"
    opinion_8 = "6, 7, 8  1"
    opinion_9 = "7, 8, 9, 101, 192, 15, 60"
    opinion_10 = "7, 8, 9, 10, 120, 15, 60, 1"
    opinion_11 = "7, 8, 9, 10, 12, 15, 60, 2"
    opinion_12 = "7, 8, 9, 10, 12, 15, 60, 2, 6"
    opinion_13 = "7, 8, 9, 10, 12, 15, 60"
    opinion_14 = "7, 8, 9, 10, 12, 15, 60, 7"
    opinion_15 = "7, 8, 9, 10,  15, 60, 90, 5"
    
    opiniones = [opinion_1, opinion_2, opinion_3, opinion_4,
             opinion_5, opinion_6, opinion_7, opinion_8, opinion_9, opinion_10, opinion_11 
             ]
    
    resultado = sistema_recomendacion(opiniones)
    
    print(resultado)
    
    return jsonify({"resultado": resultado}), 200