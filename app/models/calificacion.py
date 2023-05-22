from app import db
from sqlalchemy import func
from .historial import Historial
from app.classes.validacion import Validacion

class Calificacion(db.Model):
    cve_calificacion = db.Column(db.Integer, primary_key=True)
    calificacion_general = db.Column(db.Float, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
    
    calificacion_hotel = db.relationship('CalificacionHotel', backref='calificacion', uselist=False)
    calificacion_restaurante = db.relationship('CalificacionRestaurante', backref='calificacion', uselist=False)

    def to_dict(self):
        """
        Convertir el objeto Calificacion a un diccionario.

        Retorno:
            dict: Diccionario que representa el Calificacion.
        """
        return {
            'cve_calificacion': self.cve_calificacion,
            'calificacion_general': self.calificacion_general,
            'cve_historial': self.cve_historial
        }

    @staticmethod    
    def agregar_calificacion(cve_historial, calificacion_general):
        """
        Agregar una calificación dada por un usuario a un sitio.
        
        Entrada:
            cve_historial (int): Clave del historial.
            calificacion_general (float): Calificación al sitio.
            
        Retorno exitoso:
            True: Se ha realizado correctamente la calificación-
            
        Retorno fallido:
            False: Hubo un error o no existe un historial con la clave ingresada.
        """
        try:
            historial_encontrado = Historial.obtener_historial(cve_historial)
            
            if Validacion.valor_nulo(historial_encontrado):
                return False
            
            calificacion_nueva = Calificacion(
                calificacion_general = calificacion_general,
                cve_historial = cve_historial
            )
            db.session.add(calificacion_nueva)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un problema: ", e)
            return False

    @staticmethod
    def modificar_calificacion(cve_calificacion, calificacion_general):
        """
        Modifica la calificación general.
        
        Entrada:
            cve_calificacion (int): Clave de la calificacion.
            calificacion_general (float): Nueva calificación general a asignar.
        
        Retorno exitoso:
            True: Se modificó correctamente la calificación.
            
        Retorno fallido:
            False: Hubo un problema o no se encontró la calificación a modificar.
        """
        try:
            calificacion_encontrada = Calificacion.obtener_calificacion(cve_calificacion)
            
            if Validacion.valor_nulo(calificacion_encontrada):
                return False
            
            calificacion_encontrada.calificacion_general = calificacion_general
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un problema: ", e)
            return False
        
    @staticmethod
    def obtener_calificacion(cve_calificacion):
        """
        Consulta una calificación por su clave.

        Argumentos:
            cve_calificacion (int): Clave de la calificación a consultar.

        Retorno exitoso:
            Calificacion: Instancia de tipo Calificacion
            
        Retorno fallido:
            None: Hubo un error o no se encontró 
        """
        try:
            calificacion_encontrada = Calificacion.query.get(cve_calificacion)
        
            if Validacion.valor_nulo(calificacion_encontrada):
                return None
            else:
                return calificacion_encontrada
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_calificaciones_por_rango(rango_bajo):
        """
        Obtener calificaciones que se encuentren dentro de un rango.

        Entrada:
            rango_bajo (float): Límite inferior del rango de calificaciones a consultar.

        Retorno exitoso:
            list: Lista de instancias de tipo Calificacion.
        
        Retorno fallido:
            None: Hubo un problema o no se encontraron calificaciones que cumplan con ese filtro.
        """
        try:
            calificaciones_encontradas = Calificacion.query.filter(Calificacion.calificacion_general.between(rango_bajo, 5)).all()
        
            if Validacion.valor_nulo(calificaciones_encontradas):
                return None
            
            return calificaciones_encontradas
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_calificacion_por_historial(cve_historial):
        """
        Obtiene la calificacion por clave de historial.
        
        Entrada: 
            cve_historial (int): Clave de historial.
            
        Retorno exitoso:
            Calificacion (int): Instancia de tipo Calificacion.
            
        Retorno fallido:
            None: Hubo un error o no se encontró ninguna calificación.
        """
        try:
            calificacion_encontrada = Calificacion.query.filter_by(cve_historial=cve_historial).first()
        
            if Validacion.valor_nulo(calificacion_encontrada):
                return None
            else:
                return calificacion_encontrada
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    """
    @staticmethod
    def promedio_calificaciones_por_historial(cve_historial):
        
        Calcula el promedio de las calificaciones asociadas a un historial específico.

        Argumentos:
            cve_historial (int): Clave del historial a consultar.

        Retorno:
            dict: Diccionario con el promedio de las calificaciones si se encuentran, 
                  y un mensaje de error si no se encuentran.
        
        promedio = db.session.query(func.avg(Calificacion.calificacion_general)).filter(
            Calificacion.cve_historial == cve_historial).scalar()
        return {'promedio_calificaciones': promedio} if promedio else 'No se encontraron calificaciones para este historial', 404

    """