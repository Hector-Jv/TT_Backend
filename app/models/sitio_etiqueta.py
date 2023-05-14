from app import db
from sqlalchemy.exc import IntegrityError

class SitioEtiqueta(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )

    @classmethod
    def agregar_relacion(cls, cve_sitio, cve_etiqueta):
        """
        Método para agregar una nueva relación entre un sitio y una etiqueta.

        Argumentos:
            cve_sitio (int): Clave del sitio a relacionar.
            cve_etiqueta (int): Clave de la etiqueta a relacionar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        try:
            nueva_relacion = cls(cve_sitio=cve_sitio, cve_etiqueta=cve_etiqueta)
            db.session.add(nueva_relacion)
            db.session.commit()
            return 'Relación agregada con éxito', 200
        except IntegrityError:
            db.session.rollback()
            return 'La relación ya existe', 400

    @classmethod
    def eliminar_relacion(cls, cve_sitio, cve_etiqueta):
        """
        Método para eliminar una relación entre un sitio y una etiqueta.

        Argumentos:
            cve_sitio (int): Clave del sitio de la relación a eliminar.
            cve_etiqueta (int): Clave de la etiqueta de la relación a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        relacion = cls.query.get((cve_sitio, cve_etiqueta))
        if relacion:
            db.session.delete(relacion)
            db.session.commit()
            return 'Relación eliminada con éxito', 200
        else:
            return 'Relación no encontrada', 404

    @staticmethod
    def consultar_relaciones_por_sitio(cve_sitio):
        """
        Método para consultar todas las relaciones de un sitio por su clave.

        Argumentos:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno:
            list, int: Lista de diccionarios con las claves de las etiquetas relacionadas y código de estado HTTP.
        """
        relaciones = SitioEtiqueta.query.filter_by(cve_sitio=cve_sitio).all()
        return [{'cve_sitio': relacion.cve_sitio, 'cve_etiqueta': relacion.cve_etiqueta} for relacion in relaciones], 200

    @staticmethod
    def consultar_relaciones_por_etiqueta(cve_etiqueta):
        """
        Método para consultar todas las relaciones de una etiqueta por su clave.

        Argumentos:
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno:
            list, int: Lista de diccionarios con las claves de los sitios relacionados y código de estado HTTP.
        """
        relaciones = SitioEtiqueta.query.filter_by(cve_etiqueta=cve_etiqueta).all()
        return [{'cve_sitio': relacion.cve_sitio, 'cve_etiqueta': relacion.cve_etiqueta} for relacion in relaciones], 200
