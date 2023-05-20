from PIL import Image
import os, uuid
from flask import current_app
from werkzeug.utils import secure_filename

class Imagen():
    
    def __init__ (self, foto, nombre_ruta):
        """
        Valida y almacena los datos de una imagen.
        
        Entrada:
            foto: Es la fotografía que se desea guardar.
            nombre_ruta: Indicar el path donde se desea ubicar la foto.
            
        Retorno exitoso:
            Instancia de Imagen con los atributos foto, nombre_foto y ruta_foto.
        
        Retorno fallido:
            Mensaje con descripción de error.
            Código 400
        """
        if foto or foto.nombre:
            return "No se seleccionó ninguna foto", 400
        # Verifica que el archivo tenga una extensión válida.
        if foto and self.verificar_extension(foto.nombre):
            
            # Verifica que el tamaño de la fotografía no exceda a 1MB
            if not self.tamaño_permitido(len(foto.read())):
                return 'Foto demasiada pesada.', 400
            foto.seek(0) # Resetea el puntero
            
            # Intenta abrir la imagen.
            if not self.validar_imagen(foto):
                return 'El archivo no es una imagen válida.', 400
            foto.seek(0) # Resetea el puntero
            
            nombre_imagen = secure_filename(foto.nombre)
            nombre_unico = str(uuid.uuid4()) + "_" + nombre_imagen
            
            self.foto.save(os.path.join(current_app.config[nombre_ruta], self.nombre_foto)) # Se almacena la foto en el path especificado.
            ruta_foto = os.path.join(current_app.config[nombre_ruta], self.nombre_foto) # Se obtiene el path donde se guardó la foto.
            
            self.foto = foto
            self.nombre_foto = nombre_unico
            self.ruta_foto = ruta_foto
        else:
            return "El archivo no es una imagen.", 400
    
    def verificar_extension(filename):
        extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones_validas
        
    def tamaño_permitido(tamaño_imagen):
        tamaño_maximo = 1 * 1024 * 1024 # 1 Mb
        if tamaño_maximo > tamaño_imagen:
            return True
        return False
        
    def validar_imagen(foto):
        """
        Trata de abrir la imagen para comprobar que no haya errores.
        
        Retorno Exitoso:
            True: Se pudo abrir la imagen.
        
        Retorno Fallido:
            False: No se pudo abrir la imagen
        """
        try:
            Image.open(foto.stream) 
            return True
        except:
            return False