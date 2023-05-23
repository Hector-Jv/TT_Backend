from PIL import Image
import os
from flask import current_app
from werkzeug.utils import secure_filename

class Imagen():
    
    @staticmethod
    def verificar_extension(foto):
        """
        Verifica que la foto tenga una extensión válida.
        
        Retorno exitoso:
            True: Tiene una extensión válida.
        
        Retorno fallido:
            False: No tiene extensión válida.
        """
        extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' in foto.filename and foto.filename.rsplit('.', 1)[1].lower() in extensiones_validas:
            return True
        return False
    
    @staticmethod
    def tamaño_permitido(foto):
        tamaño_maximo = 1 * 1024 * 1024 # 1 Mb
        if tamaño_maximo > len(foto.read()):
            foto.seek(0)  # restablece el apuntador del archivo a la posición inicial
            return True
        foto.seek(0)  # restablece el apuntador del archivo a la posición inicial
        return False

    @staticmethod
    def validar_imagen(foto):
        try:
            Image.open(foto.stream)
            foto.seek(0)  # restablece el apuntador del archivo a la posición inicial
            return True
        except:
            foto.seek(0)  # restablece el apuntador del archivo a la posición inicial
            return False

    @staticmethod
    def guardar(foto, nombre, ruta):
        """
        Guarda la imagen en la ruta proporcionada.
        """
        
        carpeta = os.path.join(current_app.config[ruta], nombre)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        nombre_imagen = secure_filename(foto.filename)
        foto.save(os.path.join(carpeta, nombre_imagen).replace('\\', '/'))
        return  nombre_imagen
        