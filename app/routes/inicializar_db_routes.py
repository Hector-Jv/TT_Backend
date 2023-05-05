from flask import Blueprint, jsonify, request
from app import db
from .funciones import extraer_informacion
from app.models import TipoSitio, TipoUsuario, Delegacion, Colonia, Etiqueta, EtiquetaTipoSitio, Sitio

inicializar_blueprint = Blueprint('inicializar', __name__)

@inicializar_blueprint.route('/inicializar', methods=['GET'])
def inicializar():
    
    # Tipo sitios
    tipo_sitios = ["Museo", "Monumento", "Teatro", "Hotel", "Restaurante", "Parque"]
    
    # Se agregan a la base de datos
    for tipo_sitio in tipo_sitios:
        
        if TipoSitio.query.filter_by(tipo_sitio=tipo_sitio).first() is not None:
            continue
        
        nuevo_tipo_sitio= TipoSitio(
            tipo_sitio = tipo_sitio
        )
        
        print(f"Tipo usuario agregado: {tipo_sitio} ")
        db.session.add(nuevo_tipo_sitio)
        db.session.commit()
    
    # Tipo usuarios
    tipo_usuarios = ["Usuario registrado", "Administrador", "Cuenta eliminada"]
    
    # Se agregan a la base de datos
    for tipo_usuario in tipo_usuarios:
        
        if TipoUsuario.query.filter_by(tipo_usuario=tipo_usuario).first() is not None:
            continue
        
        nuevo_tipo_usuario = TipoUsuario(
            tipo_usuario = tipo_usuario
        )
        
        print(f"Tipo usuario agregado: {tipo_usuario} ")
        db.session.add(nuevo_tipo_usuario)
        db.session.commit()
        
    # Se agregan los municipios o delegaciones que se encontraron en el json de museos
    municipios = [
        'Gustavo A. Madero', 'Azcapotzalco', 
        'Cuajimalpa de Morelos', 'Iztacalco', 
        'Tláhuac', 'Venustiano Carranza', 
        'Coyoacán', 'Xochimilco', 
        'Iztapalapa', 'Miguel Hidalgo', 
        'Milpa Alta', 'Álvaro Obregón', 
        'Cuauhtémoc', 'Tlalpan', 
        'Benito Juárez'
    ]
    
    # Se agregan a la base de datos
    for municipio in municipios:
        
        if Delegacion.query.filter_by(nombre_delegacion=municipio).first() is not None:
            continue
        
        nuevo_municipio = Delegacion(
            nombre_delegacion = municipio
        )
        
        print(f"Tipo usuario agregado: {municipio} ")
        db.session.add(nuevo_municipio)
        db.session.commit()
    
    # Se agregan las colonias de los museos
    colonias = [('Centro ', 'Cuauhtémoc'), ('U.H. Tlatelolco, 3ra. sección', 'Cuauhtémoc'), ('Col. Tlaxpana', 'Miguel Hidalgo'), ('Col. Bosque de Chapultepec, 1a. Sección.', 'Miguel Hidalgo'), ('Col. Ciénega Grande', 'Xochimilco'), ('Col. San Pedro Mártir', 'Tlalpan'), ('Col. Daniel Garza, 2da. Sección del Bosque de Chapultepec', 'Miguel Hidalgo'), ('Col. San Diego Churubusco', 'Coyoacán'), ('Col. Doctores', 'Cuauhtémoc'), ('Col. San Pablo Tepetlapa', 'Coyoacán'), ('Col. San Miguel Chapultepec', 'Miguel Hidalgo'), ('Col. Tizapán San Ángel', 'Álvaro Obregón'), ('Col. Ampliación Daniel Garza', 'Miguel Hidalgo'), ('Col. Villa de Guadalupe', 'Gustavo A. Madero'), ('Col. Narvarte', 'Benito Juárez'), ('2do Parque las Águilas', 'Álvaro Obregón'), ('Bosque de Chapultepec', 'Miguel Hidalgo'), ('Centro', 'Cuauhtémoc'), ('Col. El Parque', 'Venustiano Carranza'), ('Col. San Andrés Tetepilco', 'Iztapalapa'), ('Col. Santa Cruz Atoyac', 'Benito Juárez'), ('Col. Cuauhtémoc dir_casacarranza@inah.gob.mx', 'Cuauhtémoc'), ('Col. Guadalupe Inn', 'Álvaro Obregón'), ('Col. Prados del Rosario', 'Azcapotzalco'), ('Col. San Miguel Chapultepec, 1ra sección', 'Miguel Hidalgo'), ('Col. Isidro Fabela', 'Tlalpan'), ('Ciudad Universitaria', 'Coyoacán'), ('Col. Santa María la Ribera', 'Cuauhtémoc'), ('Col. Chapultepec Polanco ', 'Miguel Hidalgo'), ('Col. Belén de las Flores', 'Álvaro Obregón'), ('Col. Guerrero', 'Cuauhtémoc'), ('Col. La Roma', 'Cuauhtémoc'), ('Bosque de Chapultepec 1a. Sección', 'Miguel Hidalgo'), ('Col. San Ángel Inn', 'Álvaro Obregón'), ('Col. San Andrés Míxquic', 'Tláhuac'), ('Unidad Habitacional Vicente Guerrero', 'Iztapalapa'), ('Centro', 'Cuajimalpa de Morelos'), ('Col. Roma Norte', 'Cuauhtémoc'), ('Col. 2da. del Periodista', 'Benito Juárez'), ('Col. Isla de los Sacrificios', 'Tlalpan'), ('1a. Sección del Bosque de Chapultepec', 'Miguel Hidalgo'), ('Col. Country Club', 'Coyoacán'), ('Unidad Habitacional Nonoalco-Tlatelolco, Tercera Sección', 'Cuauhtémoc'), ('Col. Nonoalco Tlatelolco', 'Cuauhtémoc'), ('Col. Culhuacán', 'Iztapalapa'), ('Col. Ampl. Veracruzana', 'Iztapalapa'), ('Col. Del Carmen', 'Coyoacán'), ('Col. Insurgentes San Borja', 'Benito Juárez'), ('Barrio La Magdalena', 'Tláhuac'), ('Col. Tepeyac Insurgentes', 'Gustavo A. Madero'), ('Col. Popotla', 'Miguel Hidalgo'), ('Barrio de Santa Catarina', 'Coyoacán'), ('Col. San Ángel', 'Álvaro Obregón'), ('Cd. Universitaria', 'Coyoacán'), ('Col. Granada', 'Miguel Hidalgo'), ('Col. Ampl. Granada', 'Miguel Hidalgo'), ('Col. La Noria', 'Xochimilco'), ('Barrio San Pablo', 'Iztapalapa'), ('Col. Zacatenco', 'Gustavo A. Madero'), ('U.H. Nonoalco-Tlaltelolco, 3ra. Sección', 'Cuauhtémoc'), ('Col. Juárez', 'Cuauhtémoc'), ('Col. Tlalpan Centro', 'Tlalpan'), ('Col. Roma', 'Cuauhtémoc'), ('Col. Bosque de Chapultepec II sección', 'Miguel Hidalgo'), ('Col. San Miguel Chapultepec,  1a. sección', 'Miguel Hidalgo'), ('Col. Tlalpan', 'Tlalpan'), ('Col. Insurgentes Mixcoac', 'Benito Juárez'), ('Col. Villa Milpa Alta', 'Milpa Alta'), ('Col. Cuauhtémoc', 'Cuauhtémoc'), ('Col. San José Ticomán', 'Gustavo A. Madero'), ('Col. San Juan de Aragón, 1a. sección', 'Gustavo A. Madero'), ('Col. Santa María La Ribera', 'Cuauhtémoc'), ('Col. Bosque de Chapultepec', 'Miguel Hidalgo'), ('U.H. Cabeza de Juárez III', 'Iztapalapa'), ('Col. Granjas México', 'Iztacalco'), ('Col. Nápoles', 'Benito Juárez'), ('Col. Tacubaya', 'Miguel Hidalgo'), ('Col. Del Carmen Coyoacán', 'Coyoacán'), ('Col. Periodista', 'Benito Juárez'), ('Col. Morelos', 'Cuauhtémoc'), ('Col. Aragón La Villa', 'Gustavo A. Madero'), ('Col. San Miguel Teotongo', 'Iztapalapa'), ('Antiguo Barrio Universitario, Centro Histórico', 'Cuauhtémoc'), ('Col. Peñón de los Baños', 'Venustiano Carranza'), ('Col. Lomas de Sotelo', 'Miguel Hidalgo'), ('Col. Tabacalera', 'Cuauhtémoc'), ('San Sebastián Tecoloxtitlán', 'Iztapalapa'), ('Pueblo de San Juan Ixtayopan', 'Tláhuac'), ('La Planta Santa Cruz Acalpixca', 'Xochimilco'), ('Col. La Venta', 'Cuajimalpa de Morelos'), ('Col. San Rafael', 'Cuauhtémoc'), ('Col. San Pedro de los Pinos', 'Benito Juárez'), ('Col. Observatorio', 'Miguel Hidalgo'), ('Col. Ex Hacienda El Rosario', 'Azcapotzalco'), ('Col. Lomas de Sotelo    ', 'Miguel Hidalgo'), ('Col. Polanco', 'Miguel Hidalgo'), ('Centro Histórico', 'Cuauhtémoc')]
    
    # Se agregan a la base de datos
    for colonia in colonias:
        
        if Colonia.query.filter_by(nombre_colonia=colonia[0]).first() is not None:
            continue
        
        nueva_colonia = Colonia(
            nombre_colonia = colonia[0],
            cve_delegacion = Delegacion.query.filter_by(nombre_delegacion=colonia[1]).first().cve_delegacion
        )
        
        print(f"Colonia agregada: {colonia} ")
        db.session.add(nueva_colonia)
        db.session.commit()
        
    # Se agregan categoría de museos
    categorias = ['Arte', 'Historia', '', 'Arqueología', 'Arte Alternativo', 'TND', 'Antropología', 'Ciencia y tecnología', 'Especializado']
    
    # Se agregan a la base de datos
    for etiqueta in categorias:
        
        if Etiqueta.query.filter_by(nombre_etiqueta=etiqueta).first() is not None:
            continue
        
        nueva_etiqueta = Etiqueta(
            nombre_etiqueta = etiqueta
        )
        
        print(f"Etiqueta agregada: {etiqueta} ")
        db.session.add(nueva_etiqueta)
        db.session.commit()
        
        # Se relacionan las categorias de los museos con el tipo de sitio
        cve_tipo_sitio = TipoSitio.query.filter_by(tipo_sitio="Museo").first().cve_tipo_sitio
        cve_etiqueta = Etiqueta.query.filter_by(nombre_etiqueta=etiqueta).first().cve_etiqueta
        
        nueva_relacion = EtiquetaTipoSitio(
            cve_tipo_sitio = cve_tipo_sitio,
            cve_etiqueta = cve_etiqueta
        )
    
        print(f"Relación creada: {cve_tipo_sitio} y {cve_etiqueta}")
        db.session.add(nueva_relacion)
        db.session.commit()
    
    # Se agregan los museos
    museos = extraer_informacion.data_lista_museos()
    
    # Se agregan a la base de datos
    for museo in museos:
        
        if Sitio.query.filter_by(nombre_sitio=museo[0]).first() is not None:
            continue
        
        nuevo_sitio = Sitio(
            nombre_sitio = 
            x_longitud = 
            y_latitud =
            direccion =
            fecha_actualizacion = 
            
            descripcion = 
            correo_sitio =
            fecha_fundacion = 
        )
        
        print(f"Etiqueta agregada: {etiqueta} ")
        db.session.add(nueva_etiqueta)
        db.session.commit()
        
        # Se relacionan las categorias de los museos con el tipo de sitio
        cve_tipo_sitio = TipoSitio.query.filter_by(tipo_sitio="Museo").first().cve_tipo_sitio
        cve_etiqueta = Etiqueta.query.filter_by(nombre_etiqueta=etiqueta).first().cve_etiqueta
        
        nueva_relacion = EtiquetaTipoSitio(
            cve_tipo_sitio = cve_tipo_sitio,
            cve_etiqueta = cve_etiqueta
        )
    
        print(f"Relación creada: {cve_tipo_sitio} y {cve_etiqueta}")
        db.session.add(nueva_relacion)
        db.session.commit()
    
    
    return jsonify({"message": "Se han inicializado los datos"}), 201

