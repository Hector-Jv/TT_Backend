from PIL import Image
import os, uuid
from flask import current_app
from werkzeug.utils import secure_filename

class Imagen():
    
    def __init__ (self, foto):
        """
        Inicializa la clase Imagen con la foto proporcionada.
        """
        self.foto = foto
        self.nombre_foto = None
        self.ruta_foto = None

    def verificar_extension(self):
        """
        Verifica que la foto tenga una extensión válida.
        
        Retorno exitoso:
            True: Tiene una extensión válida.
        
        Retorno fallido:
            False: No tiene extensión válida.
        """
        extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' in self.foto.filename and self.foto.filename.rsplit('.', 1)[1].lower() in extensiones_validas:
            return True
        return False
        
    def tamaño_permitido(self):
        """
        Verifica que la foto tenga el tamaño permitido.
        
        Retorno exitoso:
            True: Tiene un tamaño permitido.
        
        Retorno fallido:
            False: No tiene un tamaño permitido.
        """
        tamaño_maximo = 1 * 1024 * 1024 # 1 Mb
        if tamaño_maximo > len(self.foto.read()):
            return True
        return False

    def validar_imagen(self):
        """
        Trata de abrir la imagen para comprobar que no haya errores.
        
        Retorno Exitoso:
            True: Se pudo abrir la imagen.
        
        Retorno Fallido:
            False: No se pudo abrir la imagen
        """
        try:
            Image.open(self.foto.stream) 
            return True
        except:
            return False

    def guardar(self, nombre_ruta):
        """
        Guarda la imagen en la ruta proporcionada.
        """
        nombre_imagen = secure_filename(self.foto.filename)
        nombre_unico = str(uuid.uuid4()) + "_" + nombre_imagen
        
        self.foto.save(os.path.join(current_app.config[nombre_ruta], nombre_unico))
        self.ruta_foto = os.path.join(current_app.config[nombre_ruta], nombre_unico)
        
        ## self.nombre_foto = nombre_unico
