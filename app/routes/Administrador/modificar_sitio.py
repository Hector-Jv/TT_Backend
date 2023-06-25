from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, TipoUsuario, Sitio, SitioEtiqueta, ServicioHotel

modificar_sitio_bp = Blueprint('Modificar sitio', __name__)


@modificar_sitio_bp.route('/modificar_sitio', methods=['PUT'])
def ruta_modificar_sitio():
    
    ## VALIDACIONES DE ENTRADA ## 
    
    identificadores = ["correo_usuario", "cve_sitio", 
                       "nombre_sitio", "longitud",
                       "latitud", "direccion",
                       "cve_delegacion", "colonia",
                       "descripcion", "correo",
                       "costo", "pagina_web",
                       "telefono", "adscripcion",
                       "etiquetas", "servicios"]
    
    for id in identificadores:
        if id not in request.form:
            return jsonify({"error": f"El identificador {id} no se encuentra en el formulario."}), 400
    
    obligatorios = {
        "correo_usuario": request.form["correo_usuario"],
        "cve_sitio": request.form["cve_sitio"]
    }
    
    for nombre, valor in obligatorios.items():
        if not valor:
            return jsonify({"error": f"Es necesario mandar un valor valido en {nombre}."}), 400
    
    ## VALIDACION DE PERMISOS ##
    usuario_encontrado: Usuario = Usuario.query.get(obligatorios["correo_usuario"])
    if not usuario_encontrado:
        return jsonify({"error": "Es necesario ingresar con un correo registrado."}), 400
        
    tipo_usuario: TipoUsuario = TipoUsuario.query.get(usuario_encontrado.cve_tipo_usuario)
    if tipo_usuario.tipo_usuario != 'Administrador':
        return jsonify({"error": "El usuario no es administrador. No puede borrar el sitio."}), 403
    
    ## VALIDACIONES ADICIONALES ##
    sitio_encontrado: Sitio = Sitio.query.get(obligatorios['cve_sitio'])
    if not sitio_encontrado:
        return jsonify({"error": "El sitio a modificar no existe."}), 404

    ## MODIFICACION DE LOS DATOS ##
    
    try:
        sitio_encontrado.nombre_sitio = request.form['nombre_sitio']
        sitio_encontrado.longitud = request.form['longitud']
        sitio_encontrado.latitud = request.form['latitud']
        sitio_encontrado.direccion = request.form['direccion']
        sitio_encontrado.descripcion = request.form['descripcion']
        sitio_encontrado.correo = request.form['correo']
        sitio_encontrado.costo = request.form['costo']
        sitio_encontrado.pagina_web = request.form['pagina_web']
        sitio_encontrado.telefono = request.form['telefono']
        sitio_encontrado.adscripcion = request.form['adscripcion']
    except Exception as e:
        return jsonify({"error": "Hubo un error al hacer las modificaciones del sitio."}), 400
    
    try:
        if request.form['etiquetas']:
            for etiqueta in SitioEtiqueta.query.filter_by(cve_sitio=sitio_encontrado.cve_sitio).all():
                db.session.delete(etiqueta)
            
            for etiqueta in request.form['arreglo_etiquetas']:
                agregar_etiqueta: SitioEtiqueta = SitioEtiqueta(
                    sitio_encontrado.cve_sitio,
                    etiqueta["value"]
                )
                db.session.add(agregar_etiqueta)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Hubo un error al modificar las etiquetas."}), 400
    
    try:
        if request.form['servicios']:
            for servicio in ServicioHotel.query.filter_by(cve_sitio=sitio_encontrado.cve_sitio).all():
                db.session.delete(servicio)
            
            for servicio in request.form['servicios']:
                agregar_servicio: ServicioHotel = ServicioHotel(
                    sitio_encontrado.cve_sitio,
                    servicio["value"]
                )
                db.session.add(agregar_servicio)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Hubo un error al modificar las servicios."}), 400
    
    db.session.commit()
    
    return jsonify({"mensaje": "Se han modificado los datos del sitio."}), 201
    