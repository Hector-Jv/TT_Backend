from app import db
from app.classes.validacion import Validacion

class ServicioHotel(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_servicio = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_servicio'],
            ['servicio.cve_servicio'],
        ),
    )
    
    def to_dict(self):
        """
        Convertir el objeto ServicioHotel a un diccionario.

        Retorno:
            dict: Diccionario que representa el ServicioHotel.
        """
        return {
            'cve_sitio': self.cve_sitio,
            'cve_servicio': self.cve_servicio
        }

    @staticmethod
    def agregar_relacion(cve_servicio, cve_sitio):
        """
        Agregar una nueva relación entre un servicio y una hotel.

        Entrada:
            cve_sitio (int): Clave del sitio a relacionar.
            cve_servicio (int): Clave del servicio a relacionar.

        Retorno exitoso:
            True: Se ha agregado una nueva relación a la base de datos.
            
        Retorno fallido:
            False: Existe ya una relación o hubo un error.
        """
        try:
            relacion_encontrada = ServicioHotel.obtener_relacion_servicio_y_hotel(cve_servicio=cve_servicio, cve_sitio=cve_sitio)
            
            if not Validacion.valor_nulo(relacion_encontrada):
                return False
            
            nueva_relacion = ServicioHotel(
                cve_sitio=cve_sitio, 
                cve_servicio=cve_servicio
            )
            db.session.add(nueva_relacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def eliminar_relacion_por_cvesitio_y_cveservicio(cve_sitio, cve_servicio):
        """
        Eliminar una relación de la base de datos.
        
        Entrada:
            cve_sitio (int): Clave de sitio.
            cve_servicio (int): Clave de servicio.
        
        Retorno exitoso:
            True: Se elimino de manera correcta.
        
        Retorno fallido:
            False: Hubo un error
        """
        try:
            relacion_encontrada = ServicioHotel.obtener_relacion_servicio_y_hotel(cve_servicio=cve_servicio, cve_sitio=cve_sitio)

            if not Validacion.valor_nulo(relacion_encontrada):
                db.session.delete(relacion_encontrada)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def eliminar_relaciones_por_cveservicio(cve_servicio):
        """
        Eliminar todas las relaciones que tengan la misma clave de servicio.

        Entrada:
            cve_servicio (int): Clave del servicio.

        Retorno exitoso:
            True: Se han eliminado las relaciones.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            relaciones_encontradas = ServicioHotel.obtener_relaciones_por_cveservicio(cve_servicio)
            
            if Validacion.valor_nulo(relaciones_encontradas):
                return False
            
            for relacion in relaciones_encontradas:
                db.session.delete(relacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def eliminar_relaciones_por_cvesitio(cve_sitio):
        """
        Eliminar todas las relaciones que tengan la misma clave de sitio.

        Entrada:
            cve_sitio (int): Clave del sitio.

        Retorno exitoso:
            True: Se han eliminado las relaciones.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            relaciones_encontradas = ServicioHotel.obtener_relaciones_por_cvesitio(cve_sitio)
            
            if Validacion.valor_nulo(relaciones_encontradas):
                return False
            
            for relacion in relaciones_encontradas:
                db.session.delete(relacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_relaciones_por_cveservicio(cve_servicio):
        """
        Obtener todas las relaciones que tengan la misma clave servicio.

        Entrada:
            cve_servicio (int): Clave del servicio.
            
        Retorno exitoso:
            list: Lista de instancias de tipo ServicioHotel.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron relaciones.
        """
        try:
            relaciones_encontradas = ServicioHotel.query.filter_by(cve_servicio=cve_servicio).all()
            
            if not Validacion.valor_nulo(relaciones_encontradas):
                return relaciones_encontradas
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_relaciones_por_cvesitio(cve_sitio):
        """
        Obtener todas las relaciones que tengan la misma clave sitio.

        Entrada:
            cve_sitio (int): Clave del sitio.
            
        Retorno exitoso:
            list: Lista de instancias de tipo ServicioHotel.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron relaciones.
        """
        try:
            relaciones_encontradas = ServicioHotel.query.filter_by(cve_sitio=cve_sitio).all()
            
            if not Validacion.valor_nulo(relaciones_encontradas):
                return relaciones_encontradas
            else:
                return []
        except Exception as e:
            print("Hubo un error: ", e)
            return []
        
    @staticmethod
    def obtener_relacion_servicio_y_hotel(cve_servicio, cve_sitio):
        """
        Verifica si hay una relación entre un servicio y un sitio.

        Entrada:
            cve_servicio (int): Clave del servicio a consultar.
            cve_sitio (int): Clave del sitio a consultar.

        Retorno exitoso:
            ServicioHotel: Instancia ServicioHotel.
        
        Retorno fallido:
            None: No existe una relación.
        """
        try:
            relacion_encontrada = ServicioHotel.query.filter_by(cve_sitio=cve_sitio, cve_servicio=cve_servicio).first()
            if not Validacion.valor_nulo(relacion_encontrada):
                return relacion_encontrada
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        