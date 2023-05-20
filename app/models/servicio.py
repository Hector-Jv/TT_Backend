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
    
    def eliminar_servicio(self):
        """
        Método para eliminar un servicio de la base de datos.
        Antes de eliminar, verifica si existen relaciones en ServicioHotel.
        """
        relaciones = ServicioHotel.consultar_por_cve_servicio(self.cve_servicio)
        if relaciones:
            return 'No se puede eliminar el servicio porque tiene relaciones existentes en ServicioHotel', 400

        db.session.delete(self)
        db.session.commit()
    
    def modificar_servicio(self, nuevo_nombre):
        """
        Método para modificar el nombre de un servicio.

        Argumentos:
            nuevo_nombre (str): Nuevo nombre del servicio.
        """
        self.nombre_servicio = nuevo_nombre
        db.session.commit()
    
    @staticmethod
    def obtener_servicio_por_nombre(nombre_servicio):
        """
        Obtener un servicio por su nombre.

        Entrada:
            nombre_servicio (str): Nombre del servicio a buscar.

        Retorno exitoso:
            dict: Diccionario con los datos del servicio.
            
        Retorno fallido:
            None: No se encontró el servicio o hubo un error.
        """
        try:
            servicio = Servicio.query.filter_by(nombre_servicio=nombre_servicio).first()
            if servicio:
                return servicio.to_dict()
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
            dict: Diccionario con los datos del servicio.
            
        Retorno fallido:
            None: No se encontró el servicio o hubo un error.
        """
        try:
            servicio = Servicio.query.get(cve_servicio)
            if servicio:
                return servicio.to_dict()
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def consultar_todos_los_servicios():
        """
        Método estático para consultar todos los servicios existentes en la base de datos.

        Retorno:
            list, int: Lista de diccionarios con los datos de los servicios y código de estado HTTP.
        """
        servicios = Servicio.query.all()
        return [{'cve_servicio': servicio.cve_servicio, 'nombre_servicio': servicio.nombre_servicio} for servicio in servicios], 200