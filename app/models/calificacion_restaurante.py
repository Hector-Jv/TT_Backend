from app import db
from app.classes.validacion import Validacion
from .calificacion import Calificacion

class CalificacionRestaurante(db.Model):
    cve_calificacion = db.Column(db.Integer, db.ForeignKey('calificacion.cve_calificacion'), primary_key=True)
    calidad_servicio = db.Column(db.Float, nullable=False)
    sabor = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    limpieza = db.Column(db.Float, nullable=False)

    def to_dict(self):
        """
        Convertir el objeto CalificacionRestaurante a un diccionario.

        Retorno:
            dict: Diccionario que representa el CalificacionRestaurante.
        """
        return {
            'cve_calificacion': self.cve_calificacion,
            'calidad_servicio': self.calidad_servicio,
            'sabor': self.sabor,
            'costo': self.costo,
            'limpieza': self.limpieza
        }

    @staticmethod
    def agregar_calificacion(cve_calificacion, calidad_servicio, sabor, costo, limpieza):
        """
        Agrega calificación de restaurante.
        
        Entradas:
            cve_calificacion (int): Clave de calificación.
            calidad_servicio (float): Calificacion de servicio.
            sabor (float): Calificación de sabor.
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
            
            nueva_calificacion = CalificacionRestaurante(
                cve_calificacion = cve_calificacion,
                calidad_servicio = calidad_servicio,
                sabor = sabor,
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
    def modificar_calificacion(cve_calificacion, calidad_servicio=None, sabor=None, costo=None, limpieza=None):
        """
        Modifica la calificación del restaurante. Solo los argumentos que no sean None serán modificados.
        
        Entradas obligatorias:
            cve_calificacion (int): Clave de calificacion.
            
        Entradas opcionales:
            calidad_servicio (float): Nueva calificación para la calidad del servicio.
            sabor (float): Nueva calificación para el sabor.
            costo (float): Nueva calificación para el costo.
            limpieza (float): Nueva calificación para la limpieza.
            
        Retorno exitoso:
            True: Se ha hecho la modificación exitosamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            calificacion = CalificacionRestaurante.obtener_calificacionrestaurante_por_cve(cve_calificacion)
            
            if Validacion.valor_nulo(calidad_servicio):
                return False
            
            if not Validacion.valor_nulo(calidad_servicio):
                calificacion.calidad_servicio = calidad_servicio
            if not Validacion.valor_nulo(sabor):
                calificacion.sabor = sabor
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
        Eliminar calificación de un restaurante.

        Entrada:
            cve_calificacion (int): Clave de la calificación a eliminar.

        Retorno exitoso:
            True: Se ha eliminado correctamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            
            calificacion = CalificacionRestaurante.obtener_calificacionrestaurante_por_cve(cve_calificacion)
            
            if Validacion.valor_nulo(calificacion):
                return False
            
            db.session.delete(calificacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_calificacionrestaurante_por_cve(cve_calificacion):
        """
        Obtiene la calificación de un restaurante.

        Entrada:
            cve_calificacion (int): Clave de la calificación a consultar.

        Retorno exitoso:
            CalificacionRestaurante: Instancia de tipo CalificacionRestaurante.
            
        Retorno fallido:
            None: Hubo un error o no existe.
        """
        try:
            calificacion = CalificacionRestaurante.query.get(cve_calificacion)
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
            calificacion = CalificacionRestaurante.obtener_calificacionrestaurante_por_cve(cve_calificacion)
            
            if Validacion.valor_nulo(calificacion):
                return None
            
            sum_total = calificacion.calidad_servicio + calificacion.sabor + calificacion.costo + calificacion.limpieza
            return float(sum_total) / 4
        
        except Exception as e:
            print("Hubo un error: ", e)
            return None
