from app import db
from datetime import datetime

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
    
    
    def __init__(self, nombre_sitio, x_longitud, y_latitud, direccion, cve_tipo_sitio, cve_colonia, descripcion=None, correo_sitio=None, fecha_fundacion=None, costo_promedio=None, pagina_web=None, telefono=None, adscripcion=None):
        """
        Constructor de la clase Sitio.

        Argumentos:
            nombre_sitio (str): Nombre del sitio.
            x_longitud (float): Longitud del sitio.
            y_latitud (float): Latitud del sitio.
            direccion (str): Dirección del sitio.
            cve_tipo_sitio (int): Clave del tipo de sitio.
            cve_colonia (int): Clave de la colonia.
            descripcion (str, optional): Descripción del sitio. Defaults to None.
            correo_sitio (str, optional): Correo del sitio. Defaults to None.
            fecha_fundacion (datetime, optional): Fecha de fundación del sitio. Defaults to None.
            costo_promedio (float, optional): Costo promedio en el sitio. Defaults to None.
            pagina_web (str, optional): Página web del sitio. Defaults to None.
            telefono (str, optional): Teléfono del sitio. Defaults to None.
            adscripcion (str, optional): Adscripción del sitio. Defaults to None.
        """
        
        self.nombre_sitio = nombre_sitio
        self.x_longitud = x_longitud
        self.y_latitud = y_latitud
        self.direccion = direccion
        self.cve_tipo_sitio = cve_tipo_sitio
        self.cve_colonia = cve_colonia
        self.descripcion = descripcion
        self.correo_sitio = correo_sitio
        self.fecha_fundacion = fecha_fundacion
        self.costo_promedio = costo_promedio
        self.habilitado = True
        self.pagina_web = pagina_web
        self.telefono = telefono
        self.adscripcion = adscripcion
        self.fecha_actualizacion = datetime.utcnow()
        
    def actualizar_sitio(self, nombre_sitio=None, x_longitud=None, y_latitud=None, direccion=None, cve_tipo_sitio=None, cve_colonia=None, descripcion=None, correo_sitio=None, fecha_fundacion=None, costo_promedio=None, habilitado=None, pagina_web=None, telefono=None, adscripcion=None):
        """
        Método para actualizar los datos de un sitio.

        Los argumentos son opcionales, y solo se actualizarán los campos para los que se proporcione un nuevo valor.

        Argumentos:
            nombre_sitio (str, optional): Nombre del sitio. Defaults to None.
            x_longitud (float, optional): Longitud del sitio. Defaults to None.
            y_latitud (float, optional): Latitud del sitio. Defaults to None.
            direccion (str, optional): Dirección del sitio. Defaults to None.
            cve_tipo_sitio (int, optional): Clave del tipo de sitio. Defaults to None.
            cve_colonia (int, optional): Clave de la colonia. Defaults to None.
            descripcion (str, optional): Descripción del sitio. Defaults to None.
            correo_sitio (str, optional): Correo del sitio. Defaults to None.
            fecha_fundacion (datetime, optional): Fecha de fundación del sitio. Defaults to None.
            costo_promedio (float, optional): Costo promedio en el sitio. Defaults to None.
            habilitado (bool, optional): Estado de habilitado del sitio. Defaults to None.
            pagina_web (str, optional): Página web del sitio. Defaults to None.
            telefono (str, optional): Teléfono del sitio. Defaults to None.
            adscripcion (str, optional): Adscripción del sitio. Defaults to None.
        """
        
        if nombre_sitio is not None:
            self.nombre_sitio = nombre_sitio
        if x_longitud is not None:
            self.x_longitud = x_longitud
        if y_latitud is not None:
            self.y_latitud = y_latitud
        if direccion is not None:
            self.direccion = direccion
        if cve_tipo_sitio is not None:
            self.cve_tipo_sitio = cve_tipo_sitio
        if cve_colonia is not None:
            self.cve_colonia = cve_colonia
        if descripcion is not None:
            self.descripcion = descripcion
        if correo_sitio is not None:
            self.correo_sitio = correo_sitio
        if fecha_fundacion is not None:
            self.fecha_fundacion = fecha_fundacion
        if costo_promedio is not None:
            self.costo_promedio = costo_promedio
        if habilitado is not None:
            self.habilitado = habilitado
        if pagina_web is not None:
            self.pagina_web = pagina_web
        if telefono is not None:
            self.telefono = telefono
        if adscripcion is not None:
            self.adscripcion = adscripcion
        self.fecha_actualizacion = datetime.utcnow()
        db.session.commit()
        return 'Datos del sitio actualizados con éxito', 200
    
    def eliminar_sitio(self):
        """
        Método para eliminar un sitio.

        No se elimina realmente el sitio de la base de datos, solo se marca como no habilitado.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        self.habilitado = False
        db.session.commit()
        return 'Sitio eliminado con éxito', 200
    
    @staticmethod
    def consultar_sitio(cve_sitio):
        """
        Método estático para consultar un sitio por su clave.

        Argumentos:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno:
            dict, int: Diccionario con los datos del sitio y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        sitio = Sitio.query.get(cve_sitio)
        if sitio:
            return {
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
            }, 200
        return 'Sitio no encontrado', 404

    @staticmethod
    def consultar_sitios_por_tipo(cve_tipo_sitio):
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
