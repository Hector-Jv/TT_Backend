from app import db
from sqlalchemy.exc import IntegrityError

class EtiquetaTipoSitio(db.Model):
    cve_tipo_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_tipo_sitio'],
            ['tipo_sitio.cve_tipo_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )

    @classmethod
    def agregar_relacion(cls, cve_tipo_sitio, cve_etiqueta):
        """
        Método para agregar una nueva relación entre un tipo de sitio y una etiqueta.

        Argumentos:
            cve_tipo_sitio (int): Clave del tipo de sitio a relacionar.
            cve_etiqueta (int): Clave de la etiqueta a relacionar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        try:
            nueva_relacion = cls(cve_tipo_sitio=cve_tipo_sitio, cve_etiqueta=cve_etiqueta)
            db.session.add(nueva_relacion)
            db.session.commit()
            return 'Relación agregada con éxito', 200
        except IntegrityError:
            db.session.rollback()
            return 'La relación ya existe', 400

    @classmethod
    def eliminar_relacion(cls, cve_tipo_sitio, cve_etiqueta):
        """
        Método para eliminar una relación entre un tipo de sitio y una etiqueta.

        Argumentos:
            cve_tipo_sitio (int): Clave del tipo de sitio de la relación a eliminar.
            cve_etiqueta (int): Clave de la etiqueta de la relación a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        relacion = cls.query.get((cve_tipo_sitio, cve_etiqueta))
        if relacion:
            db.session.delete(relacion)
            db.session.commit()
            return 'Relación eliminada con éxito', 200
        else:
            return 'Relación no encontrada', 404

    @staticmethod
    def consultar_relaciones_por_tipo_sitio(cve_tipo_sitio):
        """
        Método para consultar todas las relaciones de un tipo de sitio por su clave.

        Argumentos:
            cve_tipo_sitio (int): Clave del tipo de sitio a consultar.

        Retorno:
            list, int: Lista de diccionarios con las claves de las etiquetas relacionadas y código de estado HTTP.
        """
        relaciones = EtiquetaTipoSitio.query.filter_by(cve_tipo_sitio=cve_tipo_sitio).all()
        return [{'cve_tipo_sitio': relacion.cve_tipo_sitio, 'cve_etiqueta': relacion.cve_etiqueta} for relacion in relaciones], 200

    @staticmethod
    def consultar_relaciones_por_etiqueta(cve_etiqueta):
        """
        Método para consultar todas las relaciones de una etiqueta por su clave.

        Argumentos:
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno:
            list, int: Lista de diccionarios con las claves de los tipos de sitio relacionados y código de estado HTTP.
        """
        relaciones = EtiquetaTipoSitio.query.filter_by(cve_etiqueta=cve_etiqueta).all()
        return [{'cve_tipo_sitio': relacion.cve_tipo_sitio, 'cve_etiqueta': relacion.cve_etiqueta} for relacion in relaciones], 200
