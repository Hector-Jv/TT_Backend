from app import db
from sqlalchemy.exc import IntegrityError
from app.classes.validacion import Validacion

class Etiqueta(db.Model):
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    nombre_etiqueta = db.Column(db.String(100), nullable=False, unique=True)

    def to_dict(self):
        """
        Convertir el objeto del etiqueta a un diccionario.

        Retorno:
            dict: Diccionario que representa la etiqueta.
        """
        return {
            'cve_etiqueta': self.cve_etiqueta,
            'nombre_etiqueta': self.nombre_etiqueta
        }


    @staticmethod
    def agregar_etiqueta(nombre_etiqueta):
        """
        Agregar una nueva etiqueta.

        Entrada:
            nombre_etiqueta (str): Nombre de la etiqueta a agregar.

        Retorno exitoso:
            True: Se ha agregado la etiqueta a la base de datos.
        
        Retorno fallido:
            False: Hubo un problema o ya existe.
        """
        try:
            etiqueta_encontrada = Etiqueta.obtener_etiqueta_por_nombre(nombre_etiqueta)
            
            if not Validacion.valor_nulo(etiqueta_encontrada):
                return False
            
            nueva_etiqueta = Etiqueta(nombre_etiqueta=nombre_etiqueta)
            db.session.add(nueva_etiqueta)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

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
    def obtener_etiqueta_por_nombre(nombre_etiqueta):
        """
        Obtener etiqueta por su nombre.

        Entrada:
            nombre_etiqueta (str): El nombre de la etiqueta a consultar.

        Retorno exitoso:
            dict: Diccionario con los datos de la etiqueta.
            
        Retorno fallido:
            None: No se encontró la etiqueta o hubo un error.
        """
        try:
            etiqueta_encontrada = Etiqueta.query.filter_by(nombre_etiqueta=nombre_etiqueta).first()
            if etiqueta_encontrada:
                return etiqueta_encontrada.to_dict()
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None