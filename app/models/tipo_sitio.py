from app import db

class TipoSitio(db.Model):
    cve_tipo_sitio = db.Column(db.Integer, primary_key=True)
    tipo_sitio = db.Column(db.String(100), nullable=False)

    def __init__(self, tipo_sitio):
        """
        Método constructor de la clase TipoSitio.

        Argumentos:
            tipo_sitio (str): Nombre del tipo de sitio.
        """
        self.tipo_sitio = tipo_sitio
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def eliminar_tipo_sitio(cve_tipo_sitio):
        """
        Método estático para eliminar un tipo de sitio.

        Argumentos:
            cve_tipo_sitio (int): Clave del tipo de sitio a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
        if tipo_sitio:
            db.session.delete(tipo_sitio)
            db.session.commit()
            return 'Tipo de sitio eliminado con éxito', 200
        return 'Tipo de sitio no encontrado', 404

    @staticmethod
    def consultar_por_cve(cve_tipo_sitio):
        """
        Método estático para consultar un tipo de sitio por su clave.

        Argumentos:
            cve_tipo_sitio (int): Clave del tipo de sitio a consultar.

        Retorno:
            dict, int: Diccionario con los datos del tipo de sitio y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
        if tipo_sitio:
            return {'tipo_sitio': tipo_sitio.tipo_sitio}, 200
        return 'Tipo de sitio no encontrado', 404

    @staticmethod
    def consultar_por_nombre(nombre):
        """
        Método estático para consultar un tipo de sitio por su nombre.

        Argumentos:
            nombre (str): Nombre del tipo de sitio a consultar.

        Retorno:
            dict, int: Diccionario con los datos del tipo de sitio y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        tipo_sitio = TipoSitio.query.filter_by(tipo_sitio=nombre).first()
        if tipo_sitio:
            return {'cve_tipo_sitio': tipo_sitio.cve_tipo_sitio}, 200
        return 'Tipo de sitio no encontrado', 404
    
    @staticmethod
    def consultar_todos():
        """
        Método estático para consultar todos los tipos de sitio.

        Returns:
            list, int: Lista de diccionarios con los datos de todos los tipos de sitio y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        tipos_sitio = TipoSitio.query.all()
        if tipos_sitio:
            return [{'cve_tipo_sitio': tipo_sitio.cve_tipo_sitio, 'tipo_sitio': tipo_sitio.tipo_sitio} for tipo_sitio in tipos_sitio], 200
        return 'No se encontraron tipos de sitio', 404


    
    