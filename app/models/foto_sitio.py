from app import db
from flask import current_app
from .sitio import Sitio
from app.classes.validacion import Validacion

class FotoSitio(db.Model):
    cve_foto_sitio = db.Column(db.Integer, autoincrement=True, nullable=False)
    nombre_imagen = db.Column(db.String(400), nullable=False)
    link_imagen = db.Column(db.String(400), nullable=True)
    nombre_autor = db.Column(db.String(400), nullable=True)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)

    def __init__(self, nombre_imagen, link_imagen, nombre_autor, cve_sitio):
        self.nombre_imagen = nombre_imagen
        self.link_imagen = link_imagen
        self.nombre_autor = nombre_autor
        self.cve_sitio = cve_sitio

    __table_args__ = (
        db.PrimaryKeyConstraint('cve_foto_sitio', 'cve_sitio'),
    )
    
    def to_dict(self):
        """
        Convertir el objeto FotoSitio a un diccionario.

        Retorno:
            dict: Diccionario que representa FotoSitio.
        """
        return {
            'cve_foto_sitio': self.cve_foto_sitio,
            'nombre_imagen': self.nombre_imagen,
            'cve_sitio': self.cve_sitio
        }
    
    @staticmethod
    def guardar_imagen(nombre_imagen, cve_sitio):
        """
        Guarda la ruta de la imagen asociada a un sitio en la base de datos.

        Entrada:
        nombre_imagen (str): Nombre de la imagen
        cve_sitio (int): La clave del sitio asociado a la imagen.

        Retorno exitoso:
            True: Se guardo correctamente.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            sitio_encontrado = Sitio.obtener_sitio_por_cve(cve_sitio)
            
            if Validacion.valor_nulo(sitio_encontrado):
                return False
        
            foto_nueva = FotoSitio(
                nombre_imagen = nombre_imagen,
                cve_sitio = cve_sitio
            )
            db.session.add(foto_nueva)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error en la funcion guardar_imagen: ", e)
            return False
    
    @staticmethod
    def eliminar_foto(cve_foto_sitio):
        """
        Elimina una foto específica.

        Entrada:
            cve_foto_sitio (int): La clave de la foto a eliminar.

        Retorno exitoso:
            True: Se elimino correctamente.
        
        Retorno fallido:
            False: Hubo un error
        """
        try:
            fotositio_encontrado = FotoSitio.query.get(cve_foto_sitio)
            
            if Validacion.valor_nulo(fotositio_encontrado):
                return False

            db.session.delete(fotositio_encontrado)
            db.session.commit()
            return True
        
        except Exception as e:
            print("Hubo un error: ",e)
            return False



    @staticmethod
    def obtener_fotositio_por_cve(cve_sitio):
        """
        Obtiene las fotos asociadas a un sitio en particular.

        Entrada:
            cve_sitio (int): La clave del sitio asociado a las imágenes.
        
        Retorno exitoso:
            FotoSitio: Instancia de tipo FotoSitio.
            
        Retorno fallido:
            None: Hubo un error o no se encuentra.
        """
        try:
            fotositio_encontrado = FotoSitio.query.filter_by(cve_sitio=cve_sitio).all()
            
            if Validacion.valor_nulo(fotositio_encontrado):
                return None
            
            return fotositio_encontrado

        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    