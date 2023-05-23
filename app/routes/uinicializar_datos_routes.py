from flask import Blueprint, jsonify, redirect, request
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import TipoSitio, Sitio, Delegacion, Colonia, Calificacion, Historial, Horario, ServicioHotel, Servicio, SitioEtiqueta, Etiqueta, FotoSitio, Usuario
from app.classes.validacion import Validacion

inicializar_bp = Blueprint('inicializar datos', __name__)

@inicializar_bp.route('/inicializar', methods=["POST"])
def inicializar_datos():
    
    ## MUSEOS ##
    Etiqueta.agregar_etiqueta("Ciencia y tecnología")
    Etiqueta.agregar_etiqueta("Arte")
    Etiqueta.agregar_etiqueta("Historia")
    Etiqueta.agregar_etiqueta("Especializado")
    Etiqueta.agregar_etiqueta("Arqueología")
    Etiqueta.agregar_etiqueta("Antropología")
    
    ## RESTAURANTES ##
    Etiqueta.agregar_etiqueta("Tacos")
    Etiqueta.agregar_etiqueta("Hamburguesas")
    Etiqueta.agregar_etiqueta("Pizzas")
    Etiqueta.agregar_etiqueta("Mariscos")
    Etiqueta.agregar_etiqueta("Cortes")
    Etiqueta.agregar_etiqueta("Buffet")
    Etiqueta.agregar_etiqueta("Música en vivo")
    Etiqueta.agregar_etiqueta("Románticos")
    Etiqueta.agregar_etiqueta("Restaurante/Bar")
    
    ## HOTELES ##
    Servicio.agregar_servicio("Alberca")
    Servicio.agregar_servicio("Estacionamiento")
    Servicio.agregar_servicio("Aire acondicionado")
    Servicio.agregar_servicio("Televisión por cable")
    Servicio.agregar_servicio("Wifi gratis")
    Servicio.agregar_servicio("Spa")
    Servicio.agregar_servicio("Bar en hotel")
    
    return jsonify({"mensaje": "Los datos han sido cargados."}), 200
    