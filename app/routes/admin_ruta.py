from flask import Blueprint, jsonify, request
from app import db
from app.models import TipoSitio, Sitio

admin_bp = Blueprint('administrador', __name__)


@admin_bp.route('/admin/crear_sitio', methods=["POST"])
def crear_sitio():
    