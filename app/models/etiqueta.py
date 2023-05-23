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

    @staticmethod
    def eliminar_etiqueta(cve_etiqueta):
        """
        Eliminar etiqueta de la base de datos.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a eliminar.

        Retorno exitoso:
            True: Se ha eliminado correctamente.
            
        Retorno fallido:
            False: Hubo un problema.
        """
        try:    
            etiqueta_encontrada = Etiqueta.query.get(cve_etiqueta)
            if etiqueta_encontrada:
                db.session.delete(etiqueta_encontrada)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un problema: ", e)
            return False

    @staticmethod
    def modificar_etiqueta(cve_etiqueta, nombre_etiqueta):
        """
        Modificar una etiqueta.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a modificar.
            nombre_etiqueta (str): Nuevo nombre de la etiqueta.

        Retorno exitoso:
            True: Se han realizado las modificaciones.
            
        Retorno fallido:
            False: Hubo un error o no existe la etiqueta a modificar.
        """
        try:
            etiqueta_encontrada = Etiqueta.query.get(cve_etiqueta)
            if etiqueta_encontrada:
                
                etiqueta_encontrada.nombre_etiqueta = nombre_etiqueta
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un problema: ", e)
            return False

    @staticmethod
    def obtener_etiqueta_por_cve(cve_etiqueta):
        """
        Obtener una etiqueta por clave.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno exitoso:
            Etiqueta: Instancia de la clase Etiqueta
            
        Retorno fallido:
            None: Hubo un error o no existe una etiqueta con la clave ingresada.
        """
        try:
            etiqueta_encontrada = Etiqueta.query.get(cve_etiqueta)
            if etiqueta_encontrada:
                return etiqueta_encontrada
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_todas_las_etiquetas():
        """
        Obtener todas las etiquetas de la base de datos.

        Retorno exitoso:
            list: Lista de instancias de tipo Etiqueta.
        
        Retorno fallido:
            list: Hubo un error o no hay etiquetas registradas.
        """
        try:  
            etiquetas_encontradas = Etiqueta.query.all()
            
            if Validacion.valor_nulo(etiquetas_encontradas):
                return []
            
            return etiquetas_encontradas
        except Exception as e:
            print("Hubo un error: ", e)
            return []

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
                return etiqueta_encontrada
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None