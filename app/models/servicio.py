from app import db
from .servicio_hotel import ServicioHotel
from app.classes.validacion import Validacion

class Servicio(db.Model):
    cve_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        """
        Convertir el objeto del Servicio a un diccionario.

        Retorno:
            dict: Diccionario que representa el Servicio.
        """
        return {
            'cve_servicio': self.cve_servicio,
            'nombre_servicio': self.nombre_servicio
        }
    
    @staticmethod
    def agregar_servicio(nombre_servicio):
        """
        Agregar un nuevo servicio a la base de datos.

        Entrada:
            nombre_servicio (str): Nombre del nuevo servicio.

        Retorno exitoso:
            True: Se ha agregado con exito a la base de datos.
            
        Retorno fallido:
            False: Ya existe o hubo un error.
        """
        try:
            servicio_encontrado = Servicio.obtener_servicio_por_nombre(nombre_servicio)
        
            if not Validacion.valor_nulo(servicio_encontrado):
                return False
            
            nuevo_servicio = Servicio(nombre_servicio=nombre_servicio)
            db.session.add(nuevo_servicio)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def eliminar_servicio(cve_servicio):
        """
        Eliminar un servicio de la base de datos.
        
        Entrada:
            cve_servicio (int): Clave del servicio.
            
        Retorno exitoso:
            True: Se ha eliminado correctamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            servicio_encontrado = Servicio.obtener_servicio_por_cve(cve_servicio)
            
            if not Validacion.valor_nulo(servicio_encontrado):
                db.session.delete(servicio_encontrado)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return False
        
    @staticmethod
    def modificar_servicio(cve_servicio, nuevo_nombre):
        """
        Modificar el nombre de un servicio.

        Entrada:
            cve_servicio (int): Clave del servicio a modificar.
            nuevo_nombre (str): Nuevo nombre del servicio.
            
        Retorno exitoso:
            True: Se ha modificado correctamente.
        
        Retorno fallido:
            False: Hubo un problema.
        """
        try:
            
            servicio_encontrado = Servicio.obtener_servicio_por_nombre(nuevo_nombre)
            
            if not Validacion.valor_nulo(servicio_encontrado):
                return False
            
            servicio_encontrado = Servicio.obtener_servicio_por_cve(cve_servicio)
            
            if Validacion.valor_nulo(servicio_encontrado):
                return False
            
            servicio_encontrado.nombre_servicio = nuevo_nombre
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
        
    @staticmethod
    def obtener_servicio_por_nombre(nombre_servicio):
        """
        Obtener un servicio por su nombre.

        Entrada:
            nombre_servicio (str): Nombre del servicio a buscar.

        Retorno exitoso:
            Servicio: Instancia de Servicio.
            
        Retorno fallido:
            None: No se encontró el servicio o hubo un error.
        """
        try:
            servicio = Servicio.query.filter_by(nombre_servicio=nombre_servicio).first()
            if not Validacion.valor_nulo(servicio):
                return servicio
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_servicio_por_cve(cve_servicio):
        """
        Obtener un servicio por su clave.

        Entrada:
            cve_servicio (int): Clave del servicio a buscar.

        Retorno exitoso:
            Servicio: Instancia de Servicio.
            
        Retorno fallido:
            None: No se encontró el servicio o hubo un error.
        """
        try:
            servicio = Servicio.query.get(cve_servicio)
            if not Validacion.valor_nulo(servicio):
                return servicio
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_todos_los_servicios():
        """
        Obtener todos los servicios existentes en la base de datos.

        Retorno exitoso:
            list: Lista de instancias de tipo Servicio.
            
        Retorno fallido:
            list: No se encontraron instancias o hubo un error.
        """
        try:
            servicios_encontrados = Servicio.query.all()

            if not Validacion.valor_nulo(servicios_encontrados):
                return servicios_encontrados
            else:
                return []
        except Exception as e:
            print("Hubo un error: ", e)
            return []