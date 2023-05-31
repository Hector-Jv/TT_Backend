from flask import Blueprint, jsonify
from app.classes.sistema_recomendacion import sistema_recomendacion
from app.classes.consulta import Consulta
from itertools import groupby
import json

generar_reglas_bp = Blueprint('Generar reglas asociacion', __name__)

@generar_reglas_bp.route('/generar_reglas', methods=['POST'])
def generar_reglas():
    
    conexion_bd = Consulta()
    
    try:
        conexion_bd.cursor.callproc('obtener_historiales')
        resultados = conexion_bd.cursor.stored_results()
        
        datos_resultado = []
        for resultado in resultados:
            datos_resultado.extend(resultado.fetchall())
    finally:
        conexion_bd.cerrar_conexion_db()
        
    
    # Se ordena por el primer elemento del par (correo, cve_sitio)
    datos_resultado.sort(key=lambda x: x[0])

    # Se agrupan por el mismo elemento
    agrupados = [list(g) for k, g in groupby(datos_resultado, lambda x: x[0])]
    
    # Extraemos solo el segundo elemento de cada par y convertimos a string
    lista_datos = [", ".join(str(x[1]) for x in sublist) for sublist in agrupados]
    print(lista_datos)

    reglas_asociacion = sistema_recomendacion(lista_datos)
    
    return jsonify({"mensaje": reglas_asociacion}), 200