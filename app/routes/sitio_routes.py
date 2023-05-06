from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Delegacion, Colonia, Horario

sitio_bp = Blueprint('sitio', __name__)

@sitio_bp.route('/sitios', methods=['GET'])
def obtener_sitios():
    
    # Se obtienen todos los sitios registrados.
    sitios = Sitio.query.all()
    
    print(sitios)
    
    # return jsonify({"sitios": sitios}), 200

@sitio_bp.route('/agregar_sitio', methods=['POST'])
def crear_sitio():
    
    # Datos recibidos del administrador.
    data = request.get_json()

    # Se extraen los datos recibidos.
    # Son obligatorios.
    nombre_sitio = data.get('nombre_sitio')
    x_longitud = data.get('x_longitud')
    y_latitud = data.get('y_latitud')
    direccion = data.get('direccion')
    
    # Llave foraneas
    tipo_sitio = data.get('tipo_sitio')
    delegacion = data.get('delegacion')
    colonia = data.get('colonia')
    
    # Pueden ser nulos.
    fecha_actualizacion = data.get('fecha_actualizacion')
    descripcion = data.get('descripcion')
    correo_sitio = data.get('correo_sitio')
    fecha_fundacion = data.get('fecha_fundacion')
    costo_promedio = data.get('costo_promedio')
    pagina_web = data.get('pagina_web')
    telefono = data.get('telefono')
    adscripcion = data.get('adscripcion')
    horarios = data.get('horarios') # Debe ser una tupla o arreglo con todos los horarios.
    
    
    
    tipo_sitio=tipo_sitio, 
    delegacion=delegacion,
    colonia=colonia, 
    horarios=horarios
    
    
    # Se crea el objeto Sitio
    sitio = Sitio(
        nombre_sitio=nombre_sitio, 
        x_longitud=x_longitud, 
        y_latitud=y_latitud,
        direccion=direccion,
        
        fecha_actualizacion=fecha_actualizacion,
        descripcion=descripcion, 
        correo_sitio=correo_sitio,
        fecha_fundacion=fecha_fundacion, 
        costo_promedio=costo_promedio,
        pagina_web=pagina_web, 
        telefono=telefono, 
        adscripcion=adscripcion
    )

    db.session.add(sitio)
    db.session.commit()
    
    