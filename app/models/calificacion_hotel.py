from app import db
from .calificacion import Calificacion
from app.classes.validacion import Validacion

class CalificacionHotel(db.Model):
    
    cve_calificacion = db.Column(db.Integer, db.ForeignKey('calificacion.cve_calificacion'), primary_key=True)
    calidad_servicio = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    limpieza = db.Column(db.Float, nullable=False)
  
    def to_dict(self):
        """
        Convertir el objeto CalificacionHotel a un diccionario.

        Retorno:
            dict: Diccionario que representa el CalificacionHotel.
        """
        return {
            'cve_calificacion': self.cve_calificacion,
            'calidad_servicio': self.calidad_servicio,
            'costo': self.costo,
            'limpieza': self.limpieza
        }

    @staticmethod
    def agregar_calificacion(cve_calificacion, calidad_servicio, costo, limpieza):
        """
        Agrega calificación de restaurante.
        
        Entradas:
            cve_calificacion (int): Clave de calificación.
            calidad_servicio (float): Calificacion de servicio.
            costo (float): Calificación de costo.
            limpieza (float): Calificación de costo.
            
        Retorno exitoso:
            True: Se agregó exitosamente.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            calificacion = Calificacion.obtener_calificacion(cve_calificacion)
            
            if Validacion.valor_nulo(calificacion):
                return False
            
            nueva_calificacion = CalificacionHotel(
                cve_calificacion = cve_calificacion,
                calidad_servicio = calidad_servicio,
                costo = costo,
                limpieza = limpieza
            )
            
            db.session.add(nueva_calificacion)
            db.session.commit()
            return True
        
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def modificar_calificacion(cve_calificacion, calidad_servicio=None, costo=None, limpieza=None):
        """
        Modifica la calificación del hotel. Solo los argumentos que no sean None serán modificados.
        
        Entradas obligatorias:
            cve_calificacion (int): Clave de calificacion.
            
        Entradas opcionales:
            calidad_servicio (float): Nueva calificación para la calidad del servicio.
            costo (float): Nueva calificación para el costo.
            limpieza (float): Nueva calificación para la limpieza.
            
        Retorno exitoso:
            True: Se ha hecho la modificación exitosamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            calificacion = CalificacionHotel.obtener_calificacionhotel_por_cve(cve_calificacion)
            
            if Validacion.valor_nulo(calidad_servicio):
                return False
            
            if not Validacion.valor_nulo(calidad_servicio):
                calificacion.calidad_servicio = calidad_servicio
            if not Validacion.valor_nulo(costo):
                calificacion.costo = costo
            if not Validacion.valor_nulo(limpieza):
                calificacion.limpieza = limpieza
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
        
    @staticmethod
    def eliminar_calificacion(cve_calificacion):
        """
        Eliminar calificación de un hotel.

        Entrada:
            cve_calificacion (int): Clave de la calificación a eliminar.

        Retorno exitoso:
            True: Se ha eliminado correctamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            
            calificacion = CalificacionHotel.obtener_calificacionhotel_por_cve(cve_calificacion)
            
            if Validacion.valor_nulo(calificacion):
                return False
            
            db.session.delete(calificacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_calificacionhotel_por_cve(cve_calificacion):
        """
        Obtiene la calificación de un hotel.

        Entrada:
            cve_calificacion (int): Clave de la calificación a consultar.

        Retorno exitoso:
            CalificacionHotel: Instancia de tipo CalificacionHotel.
            
        Retorno fallido:
            None: Hubo un error o no existe.
        """
        try:
            calificacion = CalificacionHotel.query.get(cve_calificacion)
            if calificacion:
                return calificacion
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_promedio(cve_calificacion):
        """
        Se obtiene el promedio de las calificaciones de una calificación.
        
        Entrada:
            cve_calificacion (int): Clave de calificación.
        
        Retorno exitoso:
            promedio (float): Promedio de las calificaciones.
        
        Retorno fallido:
            None: Hubo un error.
        """
        try:
            calificacion = CalificacionHotel.obtener_calificacionhotel_por_cve(cve_calificacion)
            
            if Validacion.valor_nulo(calificacion):
                return None
            
            sum_total = calificacion.calidad_servicio + calificacion.costo + calificacion.limpieza
            return float(sum_total) / 3
        
        except Exception as e:
            print("Hubo un error: ", e)
            return None
