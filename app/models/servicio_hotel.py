from app import db

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

    def __init__(self, cve_sitio, cve_servicio):
        """
        Método para inicializar una relación entre un sitio y un servicio.

        Argumentos:
            cve_sitio (int): Clave del sitio.
            cve_servicio (int): Clave del servicio.
        """
        self.cve_sitio = cve_sitio
        self.cve_servicio = cve_servicio

    def agregar_relacion(self):
        """
        Método para agregar una nueva relación a la base de datos.
        """
        db.session.add(self)
        db.session.commit()

    def eliminar_relacion(self):
        """
        Método para eliminar una relación de la base de datos.
        """
        db.session.delete(self)
        db.session.commit()

    def modificar_relacion(self, nueva_cve_sitio, nueva_cve_servicio):
        """
        Método para modificar la clave del sitio y la clave del servicio en una relación.

        Argumentos:
            nueva_cve_sitio (int): Nueva clave del sitio.
            nueva_cve_servicio (int): Nueva clave del servicio.
        """
        self.cve_sitio = nueva_cve_sitio
        self.cve_servicio = nueva_cve_servicio
        db.session.commit()
    
    @staticmethod
    def consultar_por_cve_servicio(cve_servicio):
        """
        Método estático para consultar relaciones por la clave del servicio.

        Argumentos:
            cve_servicio (int): Clave del servicio a buscar.

        Retorno:
            list, int: Lista de diccionarios con los datos de las relaciones y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        relaciones = ServicioHotel.query.filter_by(cve_servicio=cve_servicio).all()
        if relaciones:
            return [{'cve_sitio': relacion.cve_sitio, 'cve_servicio': relacion.cve_servicio} for relacion in relaciones], 200
        return 'No se encontraron relaciones con ese servicio', 404

    @staticmethod
    def consultar_por_cve_sitio(cve_sitio):
        """
        Método estático para consultar relaciones por la clave del sitio.

        Argumentos:
            cve_sitio (int): Clave del sitio a buscar.

        Retorno:
            list, int: Lista de diccionarios con los datos de las relaciones y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        relaciones = ServicioHotel.query.filter_by(cve_sitio=cve_sitio).all()
        if relaciones:
            return [{'cve_sitio': relacion.cve_sitio, 'cve_servicio': relacion.cve_servicio} for relacion in relaciones], 200
        return 'No se encontraron relaciones con ese sitio', 404
    
    @staticmethod
    def eliminar_relaciones_por_llave(cve_sitio=None, cve_servicio=None):
        """
        Método estático para eliminar todas las relaciones que tengan la misma cve_sitio o la misma cve_servicio.

        Argumentos:
            cve_sitio (int, optional): Clave del sitio. Si se proporciona, se eliminarán todas las relaciones con esta clave.
            cve_servicio (int, optional): Clave del servicio. Si se proporciona, se eliminarán todas las relaciones con esta clave.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        if cve_sitio:
            relaciones = ServicioHotel.query.filter_by(cve_sitio=cve_sitio).all()
        elif cve_servicio:
            relaciones = ServicioHotel.query.filter_by(cve_servicio=cve_servicio).all()
        else:
            return 'Debes proporcionar al menos una clave', 400

        for relacion in relaciones:
            db.session.delete(relacion)
        db.session.commit()
        return 'Relaciones eliminadas con éxito', 200

    @staticmethod
    def consultar_relaciones_por_llave(cve_sitio=None, cve_servicio=None):
        """
        Método estático para consultar todas las relaciones que tengan la misma cve_sitio o la misma cve_servicio.

        Argumentos:
            cve_sitio (int, optional): Clave del sitio. Si se proporciona, se devolverán todas las relaciones con esta clave.
            cve_servicio (int, optional): Clave del servicio. Si se proporciona, se devolverán todas las relaciones con esta clave.

        Retorno:
            list, int: Lista de diccionarios con los datos de las relaciones y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        if cve_sitio:
            relaciones = ServicioHotel.query.filter_by(cve_sitio=cve_sitio).all()
        elif cve_servicio:
            relaciones = ServicioHotel.query.filter_by(cve_servicio=cve_servicio).all()
        else:
            return 'Debes proporcionar al menos una clave', 400

        return [{'cve_sitio': relacion.cve_sitio, 'cve_servicio': relacion.cve_servicio} for relacion in relaciones], 200