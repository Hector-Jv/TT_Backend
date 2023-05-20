from app import db
from flask import current_app
from .sitio import Sitio
import os

class FotoSitio(db.Model):
    """
    Modelo de base de datos para las fotos asociadas a los sitios.

    Atributos:
    cve_foto_sitio (int): Clave primaria de la foto.
    ruta_sitio (str): Ruta donde se almacena la foto.
    cve_sitio (int): Clave foránea del sitio asociado a la foto.
    """
    
    cve_foto_sitio = db.Column(db.Integer, primary_key=True)
    ruta_sitio = db.Column(db.String(500), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    sitio = db.relationship('Sitio', backref='fotos_sitio')
    
    ## Hay que modificarlo
    @staticmethod
    def guardar_imagen(foto, cve_sitio):
        """
        Guarda una imagen asociada a un sitio en la base de datos.

        Args:
        foto (werkzeug.datastructures.FileStorage): El archivo de imagen a guardar.
        cve_sitio (int): La clave del sitio asociado a la imagen.

        Returns:
        str: Un mensaje indicando si la operación fue exitosa o no.
        int: Un código de estado HTTP indicando si la operación fue exitosa o no.
        """
        
        # Verifica que cve_sitio exista (hay que crear la función en Sitio e invocarla aqui).
        sitio = Sitio.query.get(cve_sitio)
        if sitio is None:
            return 'Sitio no válido', 400
        
        
        
        # Se verifica que se haya seleccionado un archivo.
        if foto.filename == '' or foto is None:
            return 'No se seleccionó ninguna foto.', 400
        
         # Se le añade un UUID al nombre del archivo.
            
            foto.save(os.path.join(current_app.config['IMG_SITIOS'], nombre_unico)) # Se almacena la foto en el path especificado.
            ruta_foto = os.path.join(current_app.config['IMG_SITIOS'], nombre_unico) # Se obtiene el path donde se guardó la foto.
            
            foto_sitio = FotoSitio(ruta_sitio=ruta_foto, cve_sitio=cve_sitio) # Se crea el objeto FotoComentario.
            db.session.add(foto_sitio) # Se añade el objeto a la sesión.
            db.session.commit() #Se aplican los cambios.
            return 'Foto guardada exitosamente', 200

        return 'Archivo no válido', 400
    
    
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
    
    
    
        