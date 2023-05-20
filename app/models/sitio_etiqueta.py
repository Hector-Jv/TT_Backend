from app import db
from sqlalchemy.exc import IntegrityError

class SitioEtiqueta(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_sitio'],
            ['sitio.cve_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )

    def to_dict(self):
        """
        Convertir el objeto del SitioEtiqueta a un diccionario.

        Retorno:
            dict: Diccionario que representa el SitioEtiqueta.
        """
        return {
            'cve_sitio': self.cve_sitio,
            'cve_etiqueta': self.cve_etiqueta
        }

    @staticmethod
    def agregar_relacion(cve_sitio, cve_etiqueta):
        """
        Agregar una nueva relación entre un sitio y una etiqueta.

        Entrada:
            cve_sitio (int): Clave del sitio a relacionar.
            cve_etiqueta (int): Clave de la etiqueta a relacionar.

        Retorno exitoso:
            True: Se ha agregado una nueva relación a la base de datos.
            
        Retorno fallido:
            False: Existe ya una relación o hubo un error.
        """
        try:
            if SitioEtiqueta.existe_relacion_etiqueta_y_sitio(cve_etiqueta=cve_etiqueta, cve_sitio=cve_sitio):
                return False
            
            nueva_relacion = SitioEtiqueta(
                cve_sitio=cve_sitio, 
                cve_etiqueta=cve_etiqueta
            )
            db.session.add(nueva_relacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def eliminar_relacion(cls, cve_sitio, cve_etiqueta):
        """
        Método para eliminar una relación entre un sitio y una etiqueta.

        Argumentos:
            cve_sitio (int): Clave del sitio de la relación a eliminar.
            cve_etiqueta (int): Clave de la etiqueta de la relación a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        relacion = cls.query.get((cve_sitio, cve_etiqueta))
        if relacion:
            db.session.delete(relacion)
            db.session.commit()
            return 'Relación eliminada con éxito', 200
        else:
            return 'Relación no encontrada', 404

    @staticmethod
    def consultar_relaciones_por_sitio(cve_sitio):
        """
        Método para consultar todas las relaciones de un sitio por su clave.

        Argumentos:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno:
            list, int: Lista de diccionarios con las claves de las etiquetas relacionadas y código de estado HTTP.
        """
        relaciones = SitioEtiqueta.query.filter_by(cve_sitio=cve_sitio).all()
        return [{'cve_sitio': relacion.cve_sitio, 'cve_etiqueta': relacion.cve_etiqueta} for relacion in relaciones], 200

    @staticmethod
    def obtener_relaciones_por_cveetiqueta(cve_etiqueta):
        """
        Obtener todas las relaciones de una etiqueta por su clave.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno exitoso:
            list: Lista de diccionarios con las claves de los sitios relacionados.
        
        Retorno fallido:
            None: No se encontraron relaciones o hubo un error.
        """
        try:
            relaciones_encontradas_sitioetiqueta = SitioEtiqueta.query.filter_by(cve_etiqueta=cve_etiqueta).all()
            if relaciones_encontradas_sitioetiqueta:
                return [relacion.to_dict for relacion in relaciones_encontradas_sitioetiqueta]
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        
    @staticmethod
    def existe_relacion_etiqueta_y_sitio(cve_etiqueta, cve_sitio):
        """
        Verifica si hay una relación de una etiqueta y un sitio.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a consultar.
            cve_sitio (int): Clave del sitio a consultar.

        Retorno exitoso:
            True: Existe una relación.
        
        Retorno fallido:
            False: No existe una relación.
        """
        try:
            if SitioEtiqueta.query.filter_by(cve_sitio=cve_sitio, cve_etiqueta=cve_etiqueta).first():
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return False
            
