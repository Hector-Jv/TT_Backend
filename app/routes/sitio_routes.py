from flask import Blueprint, jsonify, request
from app import db
from app.models import Sitio, Delegacion, Colonia, Horario, TipoSitio
from app.utils.validaciones import datos_necesarios

sitio_bp = Blueprint('sitio', __name__)

@sitio_bp.route('/sitios', methods=['GET'])
def obtener_sitios():
    
    # Se obtienen todos los sitios registrados.
    sitios = Sitio.query.all()
    
    lista_sitios = []
    
    for sitio in sitios:
        info_sitio = {}
        info_sitio["cve_sitio"] = sitio.cve_sitio
        info_sitio["nombre_sitio"] = sitio.nombre_sitio
        info_sitio["x_longitud"] = sitio.x_longitud
        info_sitio["y_latitud"] = sitio.y_latitud
        info_sitio["direccion"] = sitio.direccion
        info_sitio["fecha_actualizacion"] = sitio.fecha_actualizacion
        info_sitio["descripcion"] = sitio.descripcion
        info_sitio["correo_sitio"] = sitio.correo_sitio
        info_sitio["fecha_fundacion"] = sitio.fecha_fundacion
        info_sitio["costo_promedio"] = sitio.costo_promedio
        info_sitio["habilitado"] = sitio.habilitado
        info_sitio["pagina_web"] = sitio.pagina_web
        info_sitio["telefono"] = sitio.telefono
        info_sitio["adscripcion"] = sitio.adscripcion
        
        # Busca el tipo de sitio que pertenece.
        tipo_sitio_objeto = TipoSitio.query.filter_by(cve_tipo_sitio=sitio.cve_tipo_sitio).first()
        
        info_sitio["tipo_sitio"] = tipo_sitio_objeto.tipo_sitio
        info_sitio["habilitado"] = sitio.habilitado
        
        # Busca la colonia al que pertenece.
        colonia_objeto = Colonia.query.filter_by(cve_colonia=sitio.cve_colonia).first()
        
        # Busca la delegacion al que pertenece.
        delegacion_objeto = Delegacion.query.filter_by(cve_delegacion=colonia_objeto.cve_delegacion).first()
        
        info_sitio["colonia"] = colonia_objeto.nombre_colonia
        info_sitio["delegacion"] = delegacion_objeto.nombre_delegacion
        
        # Faltan las fotografías, horarios, etiquetas, servicios
        lista_sitios.append(info_sitio)
        
    return jsonify(lista_sitios), 200

@sitio_bp.route('/sitio', methods=['POST'])
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
    horarios = data.get('horarios') # Debe ser una tupla o lista con todos los horarios.
    
    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(nombre_sitio, x_longitud, y_latitud, direccion, tipo_sitio, delegacion, colonia):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    # Busca si el nombre del sitio ingresado se encuentra registrado.
    existe_sitio = Sitio.query.filter_by(nombre_sitio=nombre_sitio).first()
    
    # Se verifica que no haya un sitio registrado en la base de datos.
    if existe_sitio is not None:
        return jsonify({"error": "Ya existe el sitio ingresado."}), 404
    
    # Busca el tipo de sitio que pertenece.
    tipo_sitio_objeto = TipoSitio.query.filter_by(tipo_sitio=tipo_sitio).first()
    
    # Busca la delegacion al que pertenece.
    delegacion_objeto = Delegacion.query.filter_by(nombre_delegacion=delegacion).first()
    
    # Busca la colonia al que pertenece.
    colonia_objeto = Colonia.query.filter_by(nombre_colonia=colonia).first()
    
    # Se verifica que la colonia exista en la base de datos, sino se crea.
    if colonia_objeto is None:
        nueva_colonia = Colonia(
            nombre_colonia = colonia,
            cve_delegacion = delegacion_objeto.cve_delegacion
        )
        # Se añade la colonia a la sesión.
        db.session.add(nueva_colonia)
        # Se confirma y se aplican los cambios realizados en la base de datos.
        db.session.commit()
    
        # Busca la colonia al que pertenece.
        colonia_objeto = Colonia.query.filter_by(nombre_colonia=colonia).first()
    
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
        adscripcion=adscripcion,
        
        cve_tipo_sitio = tipo_sitio_objeto.cve_tipo_sitio,
        cve_colonia = colonia_objeto.cve_colonia
    )
    # Se añade la colonia a la sesión.
    db.session.add(sitio)
    # Se confirma y se aplican los cambios realizados en la base de datos.
    db.session.commit()
    
    # Buscamos el sitio recien ingresado.
    sitio_objeto = Sitio.query.filter_by(nombre_sitio=nombre_sitio).first()
    
    # Si se especificaron los horarios del sitio de interes.
    if horarios is not None:
        for horario in horarios:
            horario_nuevo = Horario(
                dia = horario[0],
                horario_apertura = horario[1],
                horario_cierre = horario[2],
                cve_sitio = sitio_objeto.cve_sitio
            )
            # Se añade el horario a la sesión.
            db.session.add(horario_nuevo)
            # Se confirma y se aplican los cambios realizados en la base de datos.
            db.session.commit()
    
    # Faltan las imagenes de los sitios de interés.
    
    # Si todo sale bien, regresa un json con el nombre de usuario (se va a modificar)
    return jsonify({"message": "Sitio creado con éxito"}), 201

@sitio_bp.route('/sitio', methods=['DELETE'])
def eliminar_sitio():
    
    # Datos recibidos del administrador.
    data = request.get_json()
    
    # Se extraen los datos recibidos.
    identificador_sitio = data.get('cve_sitio')
    
    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(identificador_sitio):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    # Busca si el identificador del sitio ingresado se encuentra registrado en la base de datos.
    existe_sitio = Sitio.query.filter_by(cve_sitio=identificador_sitio).first()
    
    # Se verifica que no haya un sitio registrado en la base de datos.
    if existe_sitio is None:
        return jsonify({"error": "No existe el sitio a eliminar."}), 404
    
    # Se especifica el sitio a eliminar.
    db.session.delete(existe_sitio)
    # Se confirman los cambios.
    db.session.commit()
