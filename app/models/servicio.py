from app import db
from .servicio_hotel import ServicioHotel

class Servicio(db.Model):
    cve_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(100), nullable=False)
    
    def __init__(self, nombre_servicio):
        """
        Método para inicializar un servicio.

        Argumentos:
            nombre_servicio (str): Nombre del servicio.
        """
        self.nombre_servicio = nombre_servicio
    
    def agregar_servicio(self, nombre_servicio):
        """
        Método para agregar un nuevo servicio a la base de datos.

        Argumentos:
            nombre_servicio (str): Nombre del nuevo servicio.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        servicio = Servicio.query.filter_by(nombre_servicio=nombre_servicio).first()
        if servicio:
            return 'Ya existe un servicio con ese nombre', 400
        nuevo_servicio = Servicio(nombre_servicio=nombre_servicio)
        db.session.add(nuevo_servicio)
        db.session.commit()
        return 'Servicio agregado con éxito', 200
    
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
    def consultar_por_nombre(nombre_servicio):
        """
        Método estático para consultar un servicio por su nombre.

        Argumentos:
            nombre_servicio (str): Nombre del servicio a buscar.

        Retorno:
            dict, int: Diccionario con los datos del servicio y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        servicio = Servicio.query.filter_by(nombre_servicio=nombre_servicio).first()
        if servicio:
            return {'cve_servicio': servicio.cve_servicio, 'nombre_servicio': servicio.nombre_servicio}, 200
        return 'Servicio no encontrado', 404
    
    @staticmethod
    def consultar_por_cve(cve_servicio):
        """
        Método estático para consultar un servicio por su clave.

        Argumento:
            cve_servicio (int): Clave del servicio a buscar.

        Retorno:
            dict, int: Diccionario con los datos del servicio y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        servicio = Servicio.query.get(cve_servicio)
        if servicio:
            return {'cve_servicio': servicio.cve_servicio, 'nombre_servicio': servicio.nombre_servicio}, 200
        return 'Servicio no encontrado', 404

    @staticmethod
    def consultar_todos_los_servicios():
        """
        Método estático para consultar todos los servicios existentes en la base de datos.

        Retorno:
            list, int: Lista de diccionarios con los datos de los servicios y código de estado HTTP.
        """
        servicios = Servicio.query.all()
        return [{'cve_servicio': servicio.cve_servicio, 'nombre_servicio': servicio.nombre_servicio} for servicio in servicios], 200