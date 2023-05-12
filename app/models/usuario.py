from pymysql import IntegrityError
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin
from PIL import Image # Verificación de la imagen.
import os, uuid
from sqlalchemy.orm.exc import NoResultFound
from flask import current_app
from app.models.tipo_usuario import TipoUsuario

class Usuario(db.Model, UserMixin):
    """
    Modelo de Usuario para la base de datos.
    
    Atributos:
        correo_usuario (str): Correo del usuario, sirve como clave primaria.
        usuario (str): Nombre de usuario.
        contrasena_hash  (str): Contraseña del usuario (solo para escritura, no lectura).
        foto_usuario (str): Ruta donde se almacena la foto del usuario (opcional).
        cve_tipo_usuario (int): Clave foránea del tipo de usuario.
        habilitado (bool): Indica si el usuario está habilitado o no.
        
        tipo_usuario (relationship): Relación con la tabla TipoUsuario.
    """
    correo_usuario = db.Column(db.String(100), primary_key=True, unique=True)
    usuario = db.Column(db.String(100), nullable=False, unique=True)
    contrasena_hash  = db.Column(db.String(128))
    ruta_foto_usuario = db.Column(db.String(400), nullable=True)
    cve_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.cve_tipo_usuario'), nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False)

    tipo_usuario = db.relationship('TipoUsuario', backref='usuarios')
    
    def __init__(self, correo_usuario, usuario, contrasena, foto, cve_tipo_usuario):
        self.correo_usuario = correo_usuario
        self.usuario = usuario
        self.contrasena = contrasena
        self.cve_tipo_usuario = cve_tipo_usuario
        self.habilitado = True

        if foto and self.verificar_extension(foto.filename):  
            if not self.tamaño_permitido(len(foto.read())):
                raise ValueError('Foto demasiada pesada.')
            foto.seek(0)
            
            if not self.validar_imagen(foto):
                raise ValueError('El archivo no es una imagen válida.')
            foto.seek(0)
            
            filename = secure_filename(foto.filename)
            nombre_unico = str(uuid.uuid4()) + "_" + filename
            
            foto.save(os.path.join(current_app.config['IMG_PERFIL'], nombre_unico))
            ruta_foto = os.path.join(current_app.config['IMG_PERFIL'], nombre_unico)
            self.ruta_foto_usuario = ruta_foto
    
    @property
    def contrasena(self): 
        """
        Evita la lectura directa de la contraseña.

        Raises:
            AttributeError: Siempre se lanza al intentar leer este atributo.
        """
        raise AttributeError('La contraseña no es un atributo legible')

    @contrasena.setter
    def contrasena(self, contrasena):
        """
        Define la contraseña, generando un hash para su almacenamiento seguro.

        Argumentos:
            contrasena (str): La contraseña en texto plano.
        """
        self.contrasena_hash = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        """
        Verifica la contraseña en texto plano contra el hash almacenado.

        Argumentos:
            contrasena (str): La contraseña en texto plano a verificar.

        Retorno:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password_hash(self.contrasena_hash, contrasena)
    
    def agregar_usuario(self):
        """
        Agrega el usuario actual a la base de datos.

        Retorno:
            str: Un mensaje indicando que el usuario se guardó con éxito.
            int: Un código de estado HTTP.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return 'Usuario agregado con éxito', 200
        except IntegrityError:
            db.session.rollback()
            return 'Correo o usuario ya en uso.', 400

    def actualizar_datos_cuenta(self, usuario=None, contrasena=None, foto_usuario=None):
        """
        Actualiza los datos de la cuenta del usuario con los valores proporcionados.

        Argumentos:
            usuario (str, opcional): Nuevo nombre de usuario.
            contrasena (str, opcional): Nueva contraseña.
            foto_usuario (FileStorage, opcional): Nueva foto de perfil.

        Retorno:
            str: Un mensaje indicando que los datos de la cuenta se actualizaron con éxito.
            int: Un código de estado HTTP 200.
        """
        if usuario is not None:
            self.usuario = usuario
        if contrasena is not None:
            self.contrasena = contrasena
        if foto_usuario is not None:
            if foto_usuario and Usuario.verificar_extension(foto_usuario.filename):  
                # Verifica que el tamaño de la fotografía no exceda a 1MB
                if not Usuario.tamaño_permitido(len(foto_usuario.read())):
                    return 'Foto demasiada pesada.', 400
                foto_usuario.seek(0) # Resetea el puntero
                
                if not Usuario.validar_imagen(foto_usuario):
                    return 'El archivo no es una imagen válida.', 400
                foto_usuario.seek(0) # Resetea el puntero
                
                filename = secure_filename(foto_usuario.filename)
                nombre_unico = str(uuid.uuid4()) + "_" + filename # Se le añade un UUID al nombre del archivo.
                
                # Si el usuario ya tiene una foto, elimina la foto anterior
                if self.ruta_foto_usuario:
                    try:
                        os.remove(self.ruta_foto_usuario)
                    except OSError:
                        pass
                
                foto_usuario.save(os.path.join(current_app.config['IMG_PERFIL'], nombre_unico)) # Se almacena la foto en el path especificado.
                self.ruta_foto_usuario = os.path.join(current_app.config['IMG_PERFIL'], nombre_unico) # Se actualiza la ruta en la base de datos.
            else:
                return 'Archivo no válido', 400
        db.session.commit()
        return 'Datos de la cuenta actualizados con éxito', 200

    @staticmethod
    def crear_usuario_ficticio():
        """
        Crea un usuario ficticio.

        Retorno:
            Usuario: Una instancia de Usuario con los datos del usuario ficticio.
        """
        # Genera un correo y nombre de usuario aleatorios
        correo_ficticio = f'ficticio_{uuid.uuid4()}@ficticio.com'
        usuario_ficticio = f'Usuario_{uuid.uuid4()}'
        
        # Obtiene el id del tipo de usuario "Usuario eliminado"
        cve_tipo_usuario = TipoUsuario.obtener_id_tipo_usuario('Usuario eliminado')
        if cve_tipo_usuario is None:
            return 'Tipo de usuario "Usuario eliminado" no encontrado.', 404

        # Crea el usuario ficticio
        usuario = Usuario(
            correo_usuario=correo_ficticio, 
            usuario=usuario_ficticio, 
            contrasena=str(uuid.uuid4()), # Contraseña aleatoria
            foto=None, 
            cve_tipo_usuario=cve_tipo_usuario
        )
        usuario.habilitado = False

        db.session.add(usuario)
        db.session.commit()

        return usuario 

    @staticmethod
    def consulta_por_correo(correo_usuario):
        """
        Consulta un usuario por su correo.

        Argumentos:
            correo_usuario (str): El correo del usuario a consultar.

        Retorno:
            Usuario: Una instancia de Usuario con los datos del usuario consultado.
        """
        try:
            usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).one()
            return usuario
        except NoResultFound:
            return None

    @staticmethod
    def es_usuario_habilitado(correo_usuario):
        """
        Consulta si un usuario está habilitado o no.

        Argumentos:
            correo_usuario (str): El correo del usuario a consultar.

        Retorno:
            bool: True si el usuario está habilitado, False en caso contrario.
        """
        usuario = Usuario.consulta_por_correo(correo_usuario)
        if usuario:
            return usuario.habilitado
        return False

    @staticmethod
    def consulta_por_tipo(cve_tipo_usuario):
        """
        Consulta todos los usuarios que pertenecen a un tipo de usuario determinado.

        Argumentos:
            cve_tipo_usuario (int): La clave del tipo de usuario a consultar.

        Retorno:
            list: Una lista de instancias de Usuario que pertenecen al tipo de usuario especificado.
        """
        usuarios = Usuario.query.filter_by(cve_tipo_usuario=cve_tipo_usuario).all()
        return usuarios
    
    def deshabilitar_cuenta(self):
        """
        Deshabilita la cuenta del usuario.

        Retorno:
            str: Un mensaje indicando que la cuenta se deshabilitó con éxito.
            int: Un código de estado HTTP 200.
        """
        self.habilitado = False
        db.session.commit()
        return 'Cuenta deshabilitada con éxito', 200

    @staticmethod
    def verificar_extension(filename):
        extensiones_validas = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones_validas
    
    @staticmethod
    def tamaño_permitido(tamaño_imagen):
        tamaño_maximo = 1 * 1024 * 1024 # 1 Mb
        if tamaño_maximo > tamaño_imagen:
            return True
        return False
    
    @staticmethod
    def validar_imagen(foto):
        try:
            Image.open(foto.stream) # Intenta abrir la imagen.
            return True
        except:
            return False