from app import db
from PIL import Image
import os
from werkzeug.utils import secure_filename

class FotoSitio(db.Model):
    cve_foto_sitio = db.Column(db.Integer, primary_key=True)
    foto_sitio = db.Column(db.String(500), nullable=False)
    nombre_fotografia = db.Column()
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    sitio = db.relationship('Sitio', backref='fotos_sitio')
    
    @staticmethod
    def validar_imagen(imagen):
        
        if imagen.filename == '':
            return False, "No se seleccionó ninguna imagen."
        
        if not FotoSitio.extension_permitida(imagen.filename):
            return False, "La extensión del archivo no está permitida."
        
        if not FotoSitio.size_permitido(imagen.content_length):
            return False, f"La imagen {imagen.filename} es demasiado grande."
        
        try:
            Image.open(imagen)
        except IOError:
            return False, f"El archivo {imagen.filename} no es una imagen válida."

        return True, ""
    
    def extension_permitida(archivo_imagen):
        extensiones_permitidas = {'png', 'jpg', 'jpeg'}
        # Verifica que haya un punto en el nombre del archivo y que tenga una extensión permitida
        return '.' in archivo_imagen and archivo_imagen.rsplit('.',1)[1].lower() in extensiones_permitidas

    def size_permitido(tam):
        MAX_FILE_SIZE = 1 * 1024 * 1024
        if MAX_FILE_SIZE > tam:
            return True
        return False

    @staticmethod
    def guardar_imagen(imagen, cve_sitio, app):
        filename = secure_filename(imagen.filename)

        # Crea la ruta de la carpeta del sitio
        sitio_folder_path = os.path.join(app.config['IMG_SITIOS'], str(cve_sitio))

        # Verifica si la carpeta ya existe, si no, la crea
        if not os.path.exists(sitio_folder_path):
            os.makedirs(sitio_folder_path)

        # Crea la ruta completa al archivo
        file_path = os.path.join(sitio_folder_path, filename)

        # Guarda el archivo
        imagen.save(file_path)

        # Guarda la ruta al archivo en la base de datos
        nueva_imagen = FotoSitio(
            foto_sitio = file_path,
            cve_sitio = cve_sitio
        )

        db.session.add(nueva_imagen)
        db.session.commit()
