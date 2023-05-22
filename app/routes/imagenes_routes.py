from flask import send_from_directory
from flask import Blueprint

imagenes_bp = Blueprint('imagen', __name__, url_prefix='/')

@imagenes_bp.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('../static', path)
