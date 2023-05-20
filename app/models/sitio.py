from app import db
from datetime import datetime
from .tipo_sitio import TipoSitio
from .colonia import Colonia
from app.classes.validacion import Validacion

class Sitio(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    nombre_sitio = db.Column(db.String(400), nullable=False, unique=True)
    x_longitud = db.Column(db.Float(precision=10), nullable=False)
    y_latitud = db.Column(db.Float(precision=10), nullable=False)
    direccion = db.Column(db.String(400), nullable=False)
    
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descripcion = db.Column(db.String(400), nullable=True)
    correo_sitio = db.Column(db.String(100), nullable=True)
    fecha_fundacion = db.Column(db.DateTime, nullable=True)
    costo_promedio = db.Column(db.Float(5), nullable=True)
    habilitado = db.Column(db.Boolean, default=True)
    pagina_web = db.Column(db.String(400), nullable=True)
    telefono = db.Column(db.String(30), nullable=True)
    adscripcion = db.Column(db.String(400), nullable=True)
    
    cve_tipo_sitio = db.Column(db.Integer, db.ForeignKey('tipo_sitio.cve_tipo_sitio'), nullable=False)
    cve_colonia = db.Column(db.Integer, db.ForeignKey('colonia.cve_colonia'), nullable=False)
    
    tipo_sitio = db.relationship('TipoSitio', backref='sitios')
    colonia = db.relationship('Colonia', backref='sitios')
    
    
    def to_dict(self):
        """
        Convertir el objeto del sitio a un diccionario.

        Retorno:
            dict: Diccionario que representa el sitio.
        """
        return {
            'cve_sitio': self.cve_sitio,
            'nombre_sitio': self.nombre_sitio,
            'x_longitud': self.x_longitud,
            'y_latitud': self.y_latitud,
            'direccion': self.direccion,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'descripcion': self.descripcion,
            'correo_sitio': self.correo_sitio,
            'fecha_fundacion': self.fecha_fundacion.isoformat() if self.fecha_fundacion else None,
            'costo_promedio': self.costo_promedio,
            'habilitado': self.habilitado,
            'pagina_web': self.pagina_web,
            'telefono': self.telefono,
            'adscripcion': self.adscripcion,
            'cve_tipo_sitio': self.cve_tipo_sitio,
            'cve_colonia': self.cve_colonia
        }
    
    @staticmethod
    def agregar_sitio(nombre_sitio, x_longitud, y_latitud, direccion, cve_tipo_sitio, cve_colonia, descripcion=None, correo_sitio=None, fecha_fundacion=None, costo_promedio=None, pagina_web=None, telefono=None, adscripcion=None):
        """
        Agregar un nuevo sitio a la base de datos.
        
        Entrada obligatoria:
            nombre_sitio (str): Nombre del sitio que se quiere agregar.
            x_longitud (float): Coordenada x para ubicar sitio en mapa.
            y_latitud (float): Coordenada y para ubicar sitio en mapa.
            direccion (str): Dirección en la que se encuentra el sitio.
            cve_tipo_sitio (int): Clave del tipo de sitio.
            cve_colonia (int): Clave de la colonia de sitio.
            
        Entrada opcional:
            descripcion (str): Descripción del sitio de interés.
            correo_sitio (str): Correo electrónico del sitio de interés.
            fecha_fundacion (datetime): Fecha de fundación del sitio.
            costo_promedio (float): Costo promedio en el sitio.
            pagina_web (str): Página web del sitio.
            telefono (str): Teléfono del sitio. 
            adscripcion (str): Adscripción del sitio.
            
        Retorno exitoso:
            True: Se ha guardado el sitio en la base de datos.
            
        Retorno fallido:
            False: Se produjo un error. 
        """
        if Sitio.obtener_sitio_por_nombre(nombre_sitio):
            return False
        
        if not TipoSitio.obtener_tipositio_por_cve(cve_tipo_sitio):
            return False
        
        if not Colonia.obtener_colonia_por_cve(cve_colonia):
            return False
        
        try:
            sitio = Sitio(
                nombre_sitio = nombre_sitio,
                x_longitud = x_longitud,
                y_latitud = y_latitud,
                direccion = direccion,
                cve_tipo_sitio = cve_tipo_sitio,
                cve_colonia = cve_colonia,
                descripcion = descripcion,
                correo_sitio = correo_sitio,
                fecha_fundacion = fecha_fundacion,
                costo_promedio = costo_promedio,
                habilitado = True,
                pagina_web = pagina_web,
                telefono = telefono,
                adscripcion = adscripcion,
                fecha_actualizacion = datetime.utcnow()
            )
            db.session.add(sitio)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def actualizar_sitio(cve_sitio, nombre_sitio=None, x_longitud=None, y_latitud=None, direccion=None, cve_tipo_sitio=None, cve_colonia=None, descripcion=None, correo_sitio=None, fecha_fundacion=None, costo_promedio=None, habilitado=None, pagina_web=None, telefono=None, adscripcion=None):
        """
        Actualizar los datos de un sitio.

        Entrada obligatoria:
            cve_sitio (int): Clave del sitio de interés.

        Entrada opcional:
            nombre_sitio (str): Nombre del sitio. 
            x_longitud (float): Longitud del sitio.
            y_latitud (float): Latitud del sitio.
            direccion (str): Dirección del sitio.
            cve_tipo_sitio (int): Clave del tipo de sitio.
            cve_colonia (int): Clave de la colonia.
            descripcion (str): Descripción del sitio.
            correo_sitio (str): Correo del sitio.
            fecha_fundacion (datetime): Fecha de fundación del sitio.
            costo_promedio (float): Costo promedio en el sitio.
            habilitado (bool): Estado de habilitado del sitio.
            pagina_web (str): Página web del sitio.
            telefono (str): Teléfono del sitio.
            adscripcion (str): Adscripción del sitio.
            
        Retorno exitoso:
            True: Se actualizó el sitio correctamente.
            
        Retorno fallido:
            False: Hubo un problema.
        """
        try:
            sitio_encontrado = Sitio.obtener_sitio_por_cve(cve_sitio)
            
            if Validacion.valor_nulo(sitio_encontrado):
                return False
            
            if not Validacion.valor_nulo(nombre_sitio):
                sitio_encontrado.nombre_sitio = nombre_sitio
            if not Validacion.valor_nulo(x_longitud):
                sitio_encontrado.x_longitud = x_longitud
            if not Validacion.valor_nulo(y_latitud):
                sitio_encontrado.y_latitud = y_latitud
            if not Validacion.valor_nulo(direccion):
                sitio_encontrado.direccion = direccion
            if not Validacion.valor_nulo(cve_tipo_sitio):
                sitio_encontrado.cve_tipo_sitio = cve_tipo_sitio
            if not Validacion.valor_nulo(cve_colonia):
                sitio_encontrado.cve_colonia = cve_colonia
            if not Validacion.valor_nulo(descripcion):
                sitio_encontrado.descripcion = descripcion
            if not Validacion.valor_nulo(correo_sitio):
                sitio_encontrado.correo_sitio = correo_sitio
            if not Validacion.valor_nulo(fecha_fundacion):
                sitio_encontrado.fecha_fundacion = fecha_fundacion
            if not Validacion.valor_nulo(costo_promedio):
                sitio_encontrado.costo_promedio = costo_promedio
            if not Validacion.valor_nulo(habilitado):
                sitio_encontrado.habilitado = habilitado
            if not Validacion.valor_nulo(pagina_web):
                sitio_encontrado.pagina_web = pagina_web
            if not Validacion.valor_nulo(telefono):
                sitio_encontrado.telefono = telefono
            if not Validacion.valor_nulo(adscripcion):
                sitio_encontrado.adscripcion = adscripcion
            sitio_encontrado.fecha_actualizacion = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    ## PENDIENTE ##
    @staticmethod
    def eliminar_sitio(cve_sitio):
        """
        Eliminar un sitio.

        Se sustituyen los datos personales del usuario por unos ficticios.

        Entrada:
            cve_sitio (int): Clave del sitio que se desea eliminar.
        
        Retorno exitoso:
            True: Se eliminaron los datos personales del usuario y se sustituyeron por unos ficticios.
            
        Retorno fallido:
            False: Hubo un problema al eliminar los datos del usuario.
        """
        try:
            sitio_encontrado = Sitio.obtener_sitio_por_cve(cve_sitio)
            
            if Validacion.valor_nulo(sitio_encontrado):
                return False
            
            sitio_encontrado.habilitado = False
            
            db.session.commit()
            return True
        
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def obtener_sitio_por_cve(cve_sitio):
        """
        Obtener un sitio por su clave.

        Entrada:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno exitoso:
            dict: Diccionario con los datos del sitio.
            
        Retorno fallido:
            None: No se encontró el sitio o hubo un error.
        """
        try:
            sitio = Sitio.query.get(cve_sitio)
            if sitio:
                return sitio.to_dict()
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
    
    @staticmethod
    def obtener_sitio_por_nombre(nombre_sitio):
        """
        Obtener sitio de interés por su nombre.
        
        Retorno exitoso:
            dict: Datos del sitio de interés.
        
        Retorno fallido:
            None: No se encontró el sitio de interés.
        """
        Sitio.query.filter_by(nombre_sitio=nombre_sitio).first()
    

    @staticmethod
    def obtener_sitios_por_tipo(cve_tipo_sitio):
        """
        Método estático para consultar todos los sitios que pertenecen a un cierto tipo.

        Argumentos:
            cve_tipo_sitio (int): Clave del tipo de sitio a consultar.

        Retorno:
            list, int: Lista de diccionarios con los datos de los sitios y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        sitios = Sitio.query.filter_by(cve_tipo_sitio=cve_tipo_sitio).all()
        if sitios:
            return [{
                'cve_sitio': sitio.cve_sitio,
                'nombre_sitio': sitio.nombre_sitio,
                'x_longitud': sitio.x_longitud,
                'y_latitud': sitio.y_latitud,
                'direccion': sitio.direccion,
                'descripcion': sitio.descripcion,
                'correo_sitio': sitio.correo_sitio,
                'fecha_fundacion': sitio.fecha_fundacion,
                'costo_promedio': sitio.costo_promedio,
                'pagina_web': sitio.pagina_web,
                'telefono': sitio.telefono,
                'adscripcion': sitio.adscripcion,
                'cve_tipo_sitio': sitio.cve_tipo_sitio,
                'cve_colonia': sitio.cve_colonia,
                'habilitado': sitio.habilitado
            } for sitio in sitios], 200
        return 'No se encontraron sitios con ese tipo', 404

    @staticmethod
    def consultar_sitios_por_colonia(cve_colonia):
        """
        Método estático para consultar todos los sitios que pertenecen a una cierta colonia.

        Argumentos:
            cve_colonia (int): Clave de la colonia a consultar.

        Retorno:
            list, int: Lista de diccionarios con los datos de los sitios y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        sitios = Sitio.query.filter_by(cve_colonia=cve_colonia).all()
        if sitios:
            return [{
                'nombre_sitio': sitio.nombre_sitio,
                'x_longitud': sitio.x_longitud,
                'y_latitud': sitio.y_latitud,
                'direccion': sitio.direccion,
                'descripcion': sitio.descripcion,
                'correo_sitio': sitio.correo_sitio,
                'fecha_fundacion': sitio.fecha_fundacion,
                'costo_promedio': sitio.costo_promedio,
                'pagina_web': sitio.pagina_web,
                'telefono': sitio.telefono,
                'adscripcion': sitio.adscripcion,
                'cve_tipo_sitio': sitio.cve_tipo_sitio,
                'cve_colonia': sitio.cve_colonia,
                'habilitado': sitio.habilitado
            } for sitio in sitios], 200
        return 'No se encontraron sitios en esa colonia', 404
