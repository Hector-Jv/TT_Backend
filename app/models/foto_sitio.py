from app import db
from flask import current_app
from .sitio import Sitio
import os
from app.classes.validacion import Validacion

class FotoSitio(db.Model):
    cve_foto_sitio = db.Column(db.Integer, primary_key=True)
    ruta_sitio = db.Column(db.String(500), nullable=False)
    nombre_imagen = db.Column(db.String(300), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    sitio = db.relationship('Sitio', backref='fotos_sitio')
    
    
    @staticmethod
    def guardar_imagen(ruta_sitio, nombre_imagen, cve_sitio):
        """
        Guarda la ruta de la imagen asociada a un sitio en la base de datos.

        Entrada:
        ruta_sitio (str): Ruta de la imagen
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
                ruta_sitio = ruta_sitio,
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
    def obtener_fotos_por_sitio(cve_sitio):
        """
        Obtiene las fotos asociadas a un sitio en particular.

        Args:
        cve_sitio (int): La clave del sitio asociado a las imágenes.
        
        Returns:
        list: Una lista de las rutas de las fotos asociadas al sitio.
        """
        
        fotos_sitio = FotoSitio.query.filter_by(cve_sitio=cve_sitio).all()

        if fotos_sitio:
            return [foto.ruta_sitio for foto in fotos_sitio]
        else:
            return []
    
    
    @staticmethod
    def eliminar_foto(cve_foto_sitio):
        """
        Elimina una foto específica.

        Args:
        cve_foto_sitio (int): La clave de la foto a eliminar.

        Returns:
        str: Un mensaje indicando si la eliminación fue exitosa o no.
        """
        
        foto = FotoSitio.query.get(cve_foto_sitio)

        if foto:
            os.remove(os.path.join(current_app.config['IMG_SITIOS'], foto.ruta_sitio))  # Elimina la foto del sistema de archivos.
            db.session.delete(foto)
            db.session.commit()
            return 'Foto eliminada exitosamente.'
        else:
            return 'Foto no encontrada.'
    
    
    @staticmethod
    def eliminar_fotos_sitio(cve_sitio):
        """
        Elimina todas las fotos asociadas a un sitio específico.

        Args:
        cve_sitio (int): La clave del sitio asociado a las imágenes.

        Returns:
        str: Un mensaje indicando si la eliminación fue exitosa o no.
        """
        
        fotos = FotoSitio.query.filter_by(cve_sitio=cve_sitio).all()

        if fotos:
            for foto in fotos:
                os.remove(os.path.join(current_app.config['IMG_SITIOS'], foto.ruta_sitio))
                db.session.delete(foto)
            db.session.commit()
            return 'Fotos eliminadas exitosamente.'
        else:
            return 'No se encontraron fotos para este sitio.'
    
    
    
        