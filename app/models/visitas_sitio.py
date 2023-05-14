from app import db
from sqlalchemy.exc import IntegrityError

class VisitasSitio(db.Model):
    cve_visita = db.Column(db.Integer, primary_key=True)
    fecha_visita = db.Column(db.DateTime, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    sitio = db.relationship('Sitio', backref='visitas')

    def agregar_visita(cls, fecha_visita, cve_sitio):
        """
        Método para agregar una nueva visita a un sitio.

        Argumentos:
            fecha_visita (DateTime): Fecha de la visita.
            cve_sitio (int): Clave del sitio visitado.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        try:
            nueva_visita = cls(fecha_visita=fecha_visita, cve_sitio=cve_sitio)
            db.session.add(nueva_visita)
            db.session.commit()
            return 'Visita registrada con éxito', 200
        except IntegrityError:
            db.session.rollback()
            return 'Error al registrar la visita', 400

    @staticmethod
    def consultar_visita(cve_visita):
        """
        Método para consultar una visita por clave.

        Argumentos:
            cve_visita (int): Clave de la visita a consultar.

        Retorno:
            dict, int: Diccionario con los datos de la visita y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        visita = VisitasSitio.query.get(cve_visita)
        if visita:
            return {
                'cve_visita': visita.cve_visita,
                'fecha_visita': str(visita.fecha_visita),
                'cve_sitio': visita.cve_sitio
            }, 200
        else:
            return 'Visita no encontrada', 404

    @staticmethod
    def consultar_visitas_por_sitio(cve_sitio):
        """
        Método para consultar todas las visitas a un sitio.

        Argumentos:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno:
            list, int: Lista de diccionarios con los datos de las visitas y código de estado HTTP.
        """
        visitas = VisitasSitio.query.filter_by(cve_sitio=cve_sitio).all()
        if visitas:
            return [{
                'cve_visita': visita.cve_visita,
                'fecha_visita': str(visita.fecha_visita),
                'cve_sitio': visita.cve_sitio
            } for visita in visitas], 200
        else:
            return 'No se encontraron visitas para este sitio', 404

    @staticmethod
    def consultar_visitas_por_fecha(fecha_visita):
        """
        Método para consultar todas las visitas en una fecha específica.

        Argumentos:
            fecha_visita (DateTime): Fecha de las visitas a consultar.

        Retorno:
            list, int: Lista de diccionarios con los datos de las visitas y código de estado HTTP.
        """
        visitas = VisitasSitio.query.filter_by(fecha_visita=fecha_visita).all()
        if visitas:
            return [{
                'cve_visita': visita.cve_visita,
                'fecha_visita': str(visita.fecha_visita),
                'cve_sitio': visita.cve_sitio
            } for visita in visitas], 200
        else:
            return 'No se encontraron visitas para esta fecha', 404


