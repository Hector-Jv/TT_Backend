from flask import Blueprint, jsonify, request
from app.models import TipoSitioEtiqueta, Etiqueta

mostrar_etiquetas_bp = Blueprint('mostrar_etiquetas', __name__)

@mostrar_etiquetas_bp.route('/mostrar_etiquetas/<int:cve_tipo_sitio>', methods=['GET'])
def mostrar_etiquetas(cve_tipo_sitio):
    
    ## VALIDACIONES DE ENTRADA ## 
    relacion_etiquetas = TipoSitioEtiqueta.query.filter_by(cve_tipo_sitio=cve_tipo_sitio).all()
    if not relacion_etiquetas:
        return jsonify({"mensaje": "No se encontraron etiquetas relacionadas con ese tipo sitio."}), 404
    
    arreglo_etiquetas = []
    for relacion in relacion_etiquetas:
        etiqueta: Etiqueta = Etiqueta.query.get(relacion.cve_etiqueta)
        infoEtiqueta = {}
        infoEtiqueta["cve_etiqueta"] = etiqueta.cve_etiqueta
        infoEtiqueta["nombre_etiqueta"] = etiqueta.nombre_etiqueta
        arreglo_etiquetas.append(infoEtiqueta)
        
    return jsonify(arreglo_etiquetas), 200
    
