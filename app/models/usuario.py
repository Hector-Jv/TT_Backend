import uuid
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm.exc import NoResultFound
from .tipo_usuario import TipoUsuario
from app.classes.validacion import Validacion

class Usuario(db.Model, UserMixin):
    correo_usuario = db.Column(db.String(100), primary_key=True, unique=True)
    usuario = db.Column(db.String(100), nullable=False, unique=True)
    contrasena_hash  = db.Column(db.String(128))
    ruta_foto_usuario = db.Column(db.String(400), nullable=True)
    cve_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.cve_tipo_usuario'), nullable=False)
    habilitado = db.Column(db.Boolean, nullable=False)

    tipo_usuario = db.relationship('TipoUsuario', backref='usuarios')
    
    def to_dict(self):
        """
        Convertir el objeto del Usuario a un diccionario.

        Retorno:
            dict: Diccionario que representa el Usuario.
        """
        return {
            'correo_usuario': self.correo_usuario,
            'usuario': self.usuario,
            'ruta_foto_usuario': self.ruta_foto_usuario,
            'cve_tipo_usuario': self.cve_tipo_usuario,
            'habilitado': self.habilitado
        }
    
    def verificar_contrasena(self, contrasena):
        """
        Verifica la contraseña en texto plano contra el hash almacenado.

        Entrada:
            contrasena (str): La contraseña en texto plano a verificar.

        Retorno:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password_hash(self.contrasena_hash, contrasena)
            
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

        Entrada:
            contrasena (str): La contraseña en texto plano.
        """
        self.contrasena_hash = generate_password_hash(contrasena)

    @staticmethod
    def agregar_usuario(correo_usuario, usuario, contrasena, ruta_foto_usuario):
        """
        Agrega un nuevo usuario a la base de datos.
        
        Entrada obligatoria:
            correo_usuario (str): Correo de usuario.
            usuario (str): Nombre de usuario del usuario.
            contrasena (str): Contrasena para acceder a cuenta.
        
        Entrada opcional:
            ruta_foto_usuario (str): Ruta de la imagen
            
        Retorno exitoso:
            True: Se ha creado con exito el usuario.
        
        Retorno fallido:
            False: Hubo un problema.
        """
        try:
            
            if not Validacion.valor_nulo(Usuario.obtener_usuario_por_correo(correo_usuario)):
                return False
            
            if not Validacion.valor_nulo(Usuario.obtener_usuario_por_usuario(usuario)):
                return False
            
            if not Validacion.formato_contrasena(contrasena):
                return False
            
            if not Validacion.formato_correo(correo_usuario):
                return False
            
            tipousuario_encontrado = TipoUsuario.obtener_nombre_tipo_usuario("Usuario registrado")
            
            nuevo_usuario = Usuario(
                correo_usuario = correo_usuario,
                usuario = usuario,
                contrasena = contrasena,
                ruta_foto_usuario = ruta_foto_usuario,
                cve_tipo_usuario = tipousuario_encontrado.tipo_usuario,
                habilitado = True
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return True
            
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def actualizar_datos_cuenta(correo_usuario, usuario=None, contrasena=None, ruta_foto_usuario=None):
        """
        Actualiza los datos de la cuenta del usuario con los valores proporcionados.

        Entrada obligatoria:
            correo_usuario (str): Correo de usuario.
            
        Entrada opcional:
            usuario (str): Nuevo nombre de usuario.
            contrasena (str): Nueva contraseña.
            ruta_foto_usuario (str): Nueva foto de perfil.

        Retorno exitoso:
            True: Se efectuaron los cambios correctamente.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            usuario_encontrado = Usuario.obtener_usuario_por_correo(correo_usuario)
            
            if Validacion.valor_nulo(usuario_encontrado):
                return False
            
            if not Validacion.valor_nulo(usuario):
                usuario_encontrado.usuario = usuario
            if not Validacion.valor_nulo(contrasena):
                usuario_encontrado.contrasena = contrasena
            if not Validacion.valor_nulo(ruta_foto_usuario):
                usuario_encontrado.ruta_foto_usuario = contrasena
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
            
    @staticmethod
    def eliminar_usuario(correo_usuario):
        """
        Sustituye los datos personales de la cuenta de un usuario por unos ficticios.

        Entrada:
            correo_usuario (str): Correo de usuario a eliminar.
            
        Retorno exitoso:
            True: Se han sustituido los datos por unos ficticios.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            usuario_encontrado = Usuario.obtener_usuario_por_correo(correo_usuario)
            
            if Validacion.valor_nulo(usuario_encontrado):
                return False
            
            correo_ficticio = f'ficticio_{uuid.uuid4()}@ficticio.com'
            usuario_ficticio = f'Usuario_{uuid.uuid4()}'
        
            tipousuario_encontrado = TipoUsuario.obtener_tipousuario_por_nombre("Usuario eliminado")
            
            if Validacion.valor_nulo(tipousuario_encontrado):
                return False

            usuario_encontrado.correo_usuario = correo_ficticio
            usuario_encontrado.usuario = usuario_ficticio
            usuario_encontrado.contrasena = str(uuid.uuid4())
            usuario_encontrado.ruta_foto_usuario = None
            usuario_encontrado.cve_tipo_usuario = tipousuario_encontrado.cve_tipo_usuario
            usuario_encontrado.habilitado = False
            
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un problema: ", e) 

    @staticmethod
    def obtener_usuario_por_correo(correo_usuario):
        """
        Busca un usuario por su correo.

        Entrada:
            correo_usuario (str): El correo del usuario a consultar.

        Retorno Exitoso:
            Usuario: Una instancia de Usuario con los datos del usuario consultado.
        
        Retorno Fallido:
            None: No se encontró ningún usuario con ese correo.
        """
        try:
            usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).one()
            return usuario
        except NoResultFound:
            return None

    @staticmethod
    def obtener_usuario_por_usuario(usuario):
        """
        Busca un usuario por su nombre de usuario.

        Entrada:
            usuario (str): El nombre del usuario del usuario a consultar.

        Retorno Exitoso:
            Usuario: Una instancia de Usuario con los datos del usuario consultado.
        
        Retorno Fallido:
            None: No se encontró ningún usuario con ese nombre de usuario.
        """
        try:
            usuario = Usuario.query.filter_by(usuario=usuario).one()
            return usuario
        except NoResultFound:
            return None

    @staticmethod
    def es_usuario_habilitado(correo_usuario):
        """
        Consulta si un usuario está habilitado o no.

        Entrada:
            correo_usuario (str): El correo del usuario a consultar.

        Retorno exitoso:
            True: El usuario está habilitado
            
        Retorno fallido:
            False: El usuario está deshabilitado.
        """
        try:
            usuario = Usuario.obtener_usuario_por_correo(correo_usuario)
            if usuario:
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_usuarios_por_tipousuario(cve_tipo_usuario):
        """
        Obtiene todos los usuarios que pertenecen a un tipo de usuario determinado.

        Entrada:
            cve_tipo_usuario (int): La clave del tipo de usuario a consultar.

        Retorno exitoso:
            list: Una lista de instancias de Usuario que pertenecen al tipo de usuario especificado.
            
        Retorno fallido:
            None: No se encontraron los usuarios.        
        """
        try:
            usuarios_encontrados = Usuario.query.filter_by(cve_tipo_usuario=cve_tipo_usuario).all()
            if usuarios_encontrados:
                return usuarios_encontrados
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def deshabilitar_usuario_cuenta(correo):
        """
        Deshabilita o habilita la cuenta del usuario.

        Entrada:
            correo (str): Correo de usuario a deshabilitar.
            
        Retorno exitoso:
            True: Se ha deshabilitado o habilitado la cuenta.
            
        Retorno fallido:
            False: Hubo un problema
        """
        try:
            usuario_encontrado = Usuario.obtener_usuario_por_correo(correo)
            
            if Validacion.valor_nulo(usuario_encontrado):
                return False
            
            if usuario_encontrado.habilitado:
                usuario_encontrado.habilitado = False
            else:
                usuario_encontrado.habilitado = True
            
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un problema: ", e)
            return False

