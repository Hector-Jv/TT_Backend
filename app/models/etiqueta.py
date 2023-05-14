from app import db
from sqlalchemy.exc import IntegrityError

class Etiqueta(db.Model):
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    nombre_etiqueta = db.Column(db.String(100), nullable=False, unique=True)

    def agregar_etiqueta(cls, nombre_etiqueta):
        """
        Método para agregar una nueva etiqueta.

        Argumentos:
            nombre_etiqueta (str): Nombre de la etiqueta a agregar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        try:
            nueva_etiqueta = cls(nombre_etiqueta=nombre_etiqueta)
            db.session.add(nueva_etiqueta)
            db.session.commit()
            return 'Etiqueta agregada con éxito', 200
        except IntegrityError:
            db.session.rollback()
            return 'La etiqueta ya existe', 400

    def eliminar_etiqueta(cls, cve_etiqueta):
        """
        Método para eliminar una etiqueta.

        Argumentos:
            cve_etiqueta (int): Clave de la etiqueta a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        etiqueta = cls.query.get(cve_etiqueta)
        if etiqueta:
            db.session.delete(etiqueta)
            db.session.commit()
            return 'Etiqueta eliminada con éxito', 200
        else:
            return 'Etiqueta no encontrada', 404

    def modificar_etiqueta(cls, cve_etiqueta, nombre_etiqueta):
        """
        Método para modificar una etiqueta.

        Argumentos:
            cve_etiqueta (int): Clave de la etiqueta a modificar.
            nombre_etiqueta (str): Nuevo nombre de la etiqueta.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        etiqueta = cls.query.get(cve_etiqueta)
        if etiqueta:
            try:
                etiqueta.nombre_etiqueta = nombre_etiqueta
                db.session.commit()
                return 'Etiqueta modificada con éxito', 200
            except IntegrityError:
                db.session.rollback()
                return 'La etiqueta ya existe', 400
        else:
            return 'Etiqueta no encontrada', 404

    @staticmethod
    def consultar_etiqueta_por_cve(cve_etiqueta):
        """
        Método para consultar una etiqueta por clave.

        Argumentos:
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno:
            dict, int: Diccionario con los datos de la etiqueta y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        etiqueta = Etiqueta.query.get(cve_etiqueta)
        if etiqueta:
            return {
                'cve_etiqueta': etiqueta.cve_etiqueta,
                'nombre_etiqueta': etiqueta.nombre_etiqueta
            }, 200
        else:
            return 'Etiqueta no encontrada', 404

    @staticmethod
    def consultar_todas_etiquetas():
        """
        Método para consultar todas las etiquetas existentes.

        Retorno:
            list, int: Lista de diccionarios con los datos de todas las etiquetas y código de estado HTTP.
        """
        etiquetas = Etiqueta.query.all()
        return [{
            'cve_etiqueta': etiqueta.cve_etiqueta,
            'nombre_etiqueta': etiqueta.nombre_etiqueta
        } for etiqueta in etiquetas], 200

    @staticmethod
    def consultar_etiqueta_por_nombre(nombre_etiqueta):
        """
        Método para consultar una etiqueta específica por su nombre.

        Argumentos:
            nombre_etiqueta (str): El nombre de la etiqueta a consultar.

        Retorno:
            dict, int: Diccionario con los datos de la etiqueta y código de estado HTTP, o un mensaje de error y código de estado HTTP.
        """
        etiqueta = Etiqueta.query.filter_by(nombre_etiqueta=nombre_etiqueta).first()
        if etiqueta:
            return {
                'cve_etiqueta': etiqueta.cve_etiqueta,
                'nombre_etiqueta': etiqueta.nombre_etiqueta
            }, 200
        return 'Etiqueta no encontrada', 404