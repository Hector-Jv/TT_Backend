from app import db
from app.classes.validacion import Validacion

class SitioEtiqueta(db.Model):
    cve_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, nullable=False)
    
    def __init__(self, cve_sitio:  int, cve_etiqueta: int):
        self.cve_sitio = cve_sitio
        self.cve_etiqueta = cve_etiqueta
    
    
    
    
    

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
            if SitioEtiqueta.obtener_relacion_etiqueta_y_sitio(cve_etiqueta=cve_etiqueta, cve_sitio=cve_sitio):
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
    def eliminar_relacion(cve_sitio, cve_etiqueta):
        """
        Eliminar una relación entre un sitio y una etiqueta.

        Entrada:
            cve_sitio (int): Clave del sitio de la relación a eliminar.
            cve_etiqueta (int): Clave de la etiqueta de la relación a eliminar.

        Retorno exitoso:
            True: Se elimino correctamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            relacion_encontrada = SitioEtiqueta.obtener_relacion_etiqueta_y_sitio(cve_etiqueta=cve_etiqueta, cve_sitio=cve_sitio)
        
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
    def obtener_relaciones_por_cvesitio(cve_sitio):
        """
        Obtener todas las relaciones de un sitio por su clave.

        Entrada:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno exitoso:
            list: Lista de instancia de tipo SitioEtiqueta.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron relaciones.
        """
        try:
            relaciones_encontradas = SitioEtiqueta.query.filter_by(cve_sitio=cve_sitio).all()
            if not Validacion.valor_nulo(relaciones_encontradas):
                return relaciones_encontradas
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_relaciones_por_cveetiqueta(cve_etiqueta):
        """
        Obtener todas las relaciones de una etiqueta por su clave.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno exitoso:
            list: Lista de instancias de tipo SitioEtiqueta.
        
        Retorno fallido:
            None: No se encontraron relaciones o hubo un error.
        """
        try:
            relaciones_encontradas_sitioetiqueta = SitioEtiqueta.query.filter_by(cve_etiqueta=cve_etiqueta).all()
            
            if not Validacion.valor_nulo(relaciones_encontradas_sitioetiqueta):
                return relaciones_encontradas_sitioetiqueta
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        
    @staticmethod
    def obtener_relacion_etiqueta_y_sitio(cve_etiqueta, cve_sitio):
        """
        Obtiene la relación de una etiqueta y un sitio.

        Entrada:
            cve_etiqueta (int): Clave de la etiqueta a consultar.
            cve_sitio (int): Clave del sitio a consultar.

        Retorno exitoso:
            SitioEtiqueta: Instancia SitioEtiqueta
        
        Retorno fallido:
            None: No existe una relación o hubo un error
        """
        try:
            relacion_encontrada = SitioEtiqueta.query.filter_by(cve_sitio=cve_sitio, cve_etiqueta=cve_etiqueta).first()
            if not Validacion.valor_nulo(relacion_encontrada):
                return relacion_encontrada
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
            
    