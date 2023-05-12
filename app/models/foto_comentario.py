from app import db
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image # Verificación de la imagen.
from .comentario import Comentario
import os, uuid

class FotoComentario(db.Model):
    """
    Modelo de base de datos para las fotos asociadas a los comentarios.

    Atributos:
        cve_foto_comentario (int): Clave primaria de la foto.
        ruta_foto_comentario (str): Ruta donde se almacena la foto.
        cve_comentario (int): Clave foránea del comentario asociado a la foto.
    """
    cve_foto_comentario = db.Column(db.Integer, primary_key=True)
    ruta_foto_comentario = db.Column(db.String(400), nullable=False)
    cve_comentario = db.Column(db.Integer, db.ForeignKey('comentario.cve_comentario'), nullable=False)
    
    comentario = db.relationship('Comentario', backref='fotos_comentario')
    
    
    @staticmethod
    def guardar_imagen(foto, cve_comentario):
        """
        Guarda una imagen asociada a un comentario en la base de datos.

        Argumentos:
            foto (werkzeug.datastructures.FileStorage): El archivo de imagen a guardar.
            cve_comentario (int): La clave del comentario asociado a la imagen.

        Retorno:
            str: Un mensaje indicando si la operación fue exitosa o no.
            int: Un código de estado HTTP indicando si la operación fue exitosa o no.
        """
        
        # Verifica que cve_comentario exista (hay que crear la función en Comentario e invocarla aqui).
        comentario = Comentario.query.get(cve_comentario)
        if comentario is None:
            return 'Comentario no válido', 400
        
        # Se verifica que se haya seleccionado un archivo.
        if foto.filename == '':
            return 'No se seleccionó ninguna foto.', 400
        
        # Verifica que el archivo tenga una extensión válida.
        if foto and FotoComentario.verificar_extension(foto.filename):
            
            # Verifica que el tamaño de la fotografía no exceda a 1MB
            if not FotoComentario.tamaño_permitido(len(foto.read())):
                return 'Foto demasiada pesada.', 400
            foto.seek(0) # Resetea el puntero
            
            if not FotoComentario.validar_imagen(foto):
                return 'El archivo no es una imagen válida.', 400
            foto.seek(0) # Resetea el puntero
            
            filename = secure_filename(foto.filename)
            nombre_unico = str(uuid.uuid4()) + "_" + filename # Se le añade un UUID al nombre del archivo.
            
            foto.save(os.path.join(current_app.config['IMG_COMENTARIOS'], nombre_unico)) # Se almacena la foto en el path especificado.
            ruta_foto = os.path.join(current_app.config['IMG_COMENTARIOS'], nombre_unico) # Se obtiene el path donde se guardó la foto.
            
            foto_comentario = FotoComentario(ruta_foto_comentario=ruta_foto, cve_comentario=cve_comentario) # Se crea el objeto FotoComentario.
            db.session.add(foto_comentario) # Se añade el objeto a la sesión.
            db.session.commit() #Se aplican los cambios.
            return 'Foto guardada exitosamente', 200

        return 'Archivo no válido', 400
    
    
    @staticmethod
    def obtener_fotos_por_comentario(cve_comentario):
        """
        Obtiene las fotos asociadas a un comentario en particular.

        Args:
        cve_comentario (int): La clave del comentario asociado a las imágenes.
        
        Returns:
        list: Una lista de las rutas de las fotos asociadas al comentario.
        """
        
        fotos_comentario = FotoComentario.query.filter_by(cve_comentario=cve_comentario).all()

        if fotos_comentario:
            return [foto.ruta_foto_comentario for foto in fotos_comentario]
        else:
            return []
    
    
    @staticmethod
    def eliminar_foto(cve_foto_comentario):
        """
        Elimina una foto específica.

        Args:
        cve_foto_comentario (int): La clave de la foto a eliminar.

        Returns:
        str: Un mensaje indicando si la eliminación fue exitosa o no.
        """
        
        foto = FotoComentario.query.get(cve_foto_comentario)

        if foto:
            os.remove(os.path.join(current_app.config['IMG_COMENTARIOS'], foto.ruta_foto_comentario))  # Elimina la foto del sistema de archivos.
            db.session.delete(foto)
            db.session.commit()
            return 'Foto eliminada exitosamente.'
        else:
            return 'Foto no encontrada.'
    
    
    @staticmethod
    def eliminar_fotos_comentario(cve_comentario):
        """
        Elimina todas las fotos asociadas a un comentario específico.

        Args:
        cve_comentario (int): La clave del comentario asociado a las imágenes.

        Returns:
        str: Un mensaje indicando si la eliminación fue exitosa o no.
        """
        
        fotos = FotoComentario.query.filter_by(cve_comentario=cve_comentario).all()

        if fotos:
            for foto in fotos:
                os.remove(os.path.join(current_app.config['IMG_COMENTARIOS'], foto.ruta_foto_comentario))
                db.session.delete(foto)
            db.session.commit()
            return 'Fotos eliminadas exitosamente.'
        else:
            return 'No se encontraron fotos para este comentario.'
    
    
    def verificar_extension(filename):
        extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones_validas
        
    def tamaño_permitido(tamaño_imagen):
        tamaño_maximo = 1 * 1024 * 1024 # 1 Mb
        if tamaño_maximo > tamaño_imagen:
            return True
        return False
        
    def validar_imagen(foto):
        try:
            Image.open(foto.stream) # Intenta abrir la imagen.
            return True
        except:
            return False
        