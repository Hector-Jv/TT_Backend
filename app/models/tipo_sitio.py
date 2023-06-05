from app import db

class TipoSitio(db.Model):
    cve_tipo_sitio = db.Column(db.Integer, primary_key=True)
    tipo_sitio = db.Column(db.String(100), nullable=False)
    
    def __init__(self, tipo_sitio):
        self.tipo_sitio = tipo_sitio
    
    
    def to_dict(self):
        """
        Convertir el objeto TipoSitio a un diccionario.

        Retorno:
            dict: Diccionario que representa el TipoSitio.
        """
        return {
            'cve_tipo_sitio': self.cve_tipo_sitio,
            'tipo_sitio': self.tipo_sitio
        }

    @staticmethod
    def agregar_tipositio(tipo_sitio):
        """
        Agrega un nuevo tipo sitio a la base de datos.
        
        Entrada:
            tipo_sitio (str): Nombre del tipo sitio.
            
        Retorno exitoso:
            True: Se agregó el tipo sitio exitosamente a la base de datos.
            
        Retorno fallido:
            False: Hubo un problema al querer agregarlo.
        """
        if TipoSitio.obtener_tipositio_por_nombre(tipo_sitio):
            return False
        
        try:
            nuevo_tipositio = TipoSitio(tipo_sitio=tipo_sitio)
            db.session.add(nuevo_tipositio)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un problema: ", e)
            return False

    @staticmethod
    def eliminar_tipositio(cve_tipo_sitio):
        """
        Eliminar un tipo de sitio.

        Entrada:
            cve_tipo_sitio (int): Clave del tipo de sitio a eliminar.

        Retorno exitoso:
            True: Se eliminó el sitio de la base de datos.
            
        Retorno fallido:
            False: Ocurrió un problema y no se pudo eliminar.
        """
        try:
            tipo_sitio = TipoSitio.obtener_tipositio_por_cve(cve_tipo_sitio)
            if tipo_sitio:
                db.session.delete(tipo_sitio)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_tipositio_por_cve(cve_tipo_sitio):
        """
        Obtener el tipo de sitio por su clave.

        Entrada:
            cve_tipo_sitio (int): Clave del tipo de sitio a consultar.

        Retorno exitoso:
            TipoSitio: Objeto TipoSitio.
        
        Retorno fallido:
            None: No se encontró el tipo de sitio.
        """
        try:
            tipo_sitio = TipoSitio.query.get(cve_tipo_sitio)
            if tipo_sitio:
                return tipo_sitio
            else:
                return None
        except Exception as e:
            print("Hubo un error en función obtener_tipositio_por_cve: ", e)
            return None

    @staticmethod
    def obtener_tipositio_por_nombre(nombre):
        """
        Obtener el tipo de sitio por su nombre.

        Entrada:
            nombre (str): Nombre del tipo de sitio a consultar.

        Retorno exitoso:
            TipoSitio: Instancia TipoSitio.
        
        Retorno fallido:
            None: No se encontraron los datos del tipo de sitio.
        """
        try:
            tipo_sitio = TipoSitio.query.filter_by(tipo_sitio=nombre).first()
            if tipo_sitio:
                return tipo_sitio
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_tipositios():
        """
        Obtener todos los tipos de sitio.

        Retorno exitoso:
            list: Lista de instancia de TipoSitio.
        
        Retorno fallido:
            None: No se encontraron tipos de sitios o hubo un error.
        """
        try:
            tipos_sitio = TipoSitio.query.all()
            if tipos_sitio:
                return tipos_sitio
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
