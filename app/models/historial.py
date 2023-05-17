from datetime import datetime
from sqlalchemy import func
from app import db

class Historial(db.Model):
    cve_historial = db.Column(db.Integer, primary_key=True)
    me_gusta = db.Column(db.Boolean, default=False)
    fecha_visita = db.Column(db.DateTime, nullable=False)
    cve_usuario = db.Column(db.String(100), db.ForeignKey('usuario.correo_usuario'), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    usuario = db.relationship('Usuario', backref='historiales')
    sitio = db.relationship('Sitio', backref='historiales')

    def __init__(self, cve_usuario, cve_sitio):
        """
        Constructor del historial.

        Argumentos:
            cve_usuario (str): Clave del usuario que realiza la visita.
            cve_sitio (int): Clave del sitio visitado.
        """
        self.cve_usuario = cve_usuario
        self.cve_sitio = cve_sitio
        self.me_gusta = False
        self.fecha_visita = datetime.now()

    def modificar_me_gusta(self, me_gusta):
        """
        Modifica el estado de "me_gusta" del historial.

        Argumentos:
            me_gusta (bool): Nuevo estado de "me_gusta".
        """
        self.me_gusta = me_gusta
        db.session.commit()

    @staticmethod
    def consultar_historial(cve_historial):
        """
        Consulta un historial por su clave.

        Argumentos:
            cve_historial (int): Clave del historial.

        Retorno:
            dict, int: Diccionario con los datos del historial si es encontrado, y código de estado HTTP.
        """
        historial = Historial.query.get(cve_historial)
        if historial:
            return {
                'cve_historial': historial.cve_historial,
                'me_gusta': historial.me_gusta,
                'fecha_visita': historial.fecha_visita,
                'cve_usuario': historial.cve_usuario,
                'cve_sitio': historial.cve_sitio,
            }, 200
        return 'Historial no encontrado', 404

    @staticmethod
    def consultar_historiales_por_sitio(cve_sitio):
        """
        Consulta todos los historiales asociados a un sitio.

        Argumentos:
            cve_sitio (int): Clave del sitio.

        Retorno:
            list, int: Lista de diccionarios con los datos de los historiales si son encontrados, y código de estado HTTP.
        """
        historiales = Historial.query.filter_by(cve_sitio=cve_sitio).all()
        if historiales:
            return [{
                'cve_historial': historial.cve_historial,
                'me_gusta': historial.me_gusta,
                'fecha_visita': historial.fecha_visita,
                'cve_usuario': historial.cve_usuario,
                'cve_sitio': historial.cve_sitio,
            } for historial in historiales], 200
        return None, 404
    
    @staticmethod
    def consultar_historiales_por_usuario(cve_usuario):
        """
        Consulta todos los historiales asociados a un usuario.

        Argumentos:
            cve_usuario (str): Clave del usuario.

        Retorno:
            list, int: Lista de diccionarios con los datos de los historiales si son encontrados, y código de estado HTTP.
        """
        historiales = Historial.query.filter_by(cve_usuario=cve_usuario).all()
        if historiales:
            return [{
                'cve_historial': historial.cve_historial,
                'me_gusta': historial.me_gusta,
                'fecha_visita': historial.fecha_visita,
                'cve_usuario': historial.cve_usuario,
                'cve_sitio': historial.cve_sitio,
            } for historial in historiales], 200
        return 'No se encontraron historiales para este usuario', 404
    
    @staticmethod
    def consultar_historiales_recientes():
        """
        Consulta todos los historiales ordenados de manera descendente por fecha de visita.

        Retorno:
            list, int: Lista de diccionarios con los datos de los historiales.
        """
        historiales = Historial.query.order_by(Historial.fecha_visita.desc()).all()
        return [{
            'cve_historial': historial.cve_historial,
            'me_gusta': historial.me_gusta,
            'fecha_visita': historial.fecha_visita,
            'cve_usuario': historial.cve_usuario,
            'cve_sitio': historial.cve_sitio,
        } for historial in historiales], 200
        
    @staticmethod
    def consultar_historiales_por_me_gusta(cve_usuario, me_gusta):
        """
        Consulta todos los historiales de un usuario que coinciden con una preferencia "me_gusta".

        Argumentos:
            cve_usuario (str): Clave del usuario.
            me_gusta (bool): Preferencia de "me_gusta".

        Retorno:
            list, int: Lista de diccionarios con los datos de los historiales si son encontrados, y código de estado HTTP.
        """
        historiales = Historial.query.filter_by(cve_usuario=cve_usuario, me_gusta=me_gusta).all()
        if historiales:
            return [{
                'cve_historial': historial.cve_historial,
                'me_gusta': historial.me_gusta,
                'fecha_visita': historial.fecha_visita,
                'cve_usuario': historial.cve_usuario,
                'cve_sitio': historial.cve_sitio,
            } for historial in historiales], 200
        return 'No se encontraron historiales que coincidan con la preferencia', 404
    

    @staticmethod
    def contar_visitas_por_sitio_en_fecha(cve_sitio, fecha_inicio, fecha_fin):
        """
        Cuenta las visitas a un sitio en un rango de fechas.

        Argumentos:
            cve_sitio (int): Clave del sitio.
            fecha_inicio (datetime): Fecha de inicio del rango.
            fecha_fin (datetime): Fecha de fin del rango.

        Retorno:
            dict: Diccionario con la cantidad de visitas.
        """
        count = db.session.query(func.count(Historial.cve_historial)).filter(
            Historial.cve_sitio == cve_sitio,
            Historial.fecha_visita >= fecha_inicio,
            Historial.fecha_visita <= fecha_fin
        ).scalar()
        return {'visitas': count}




