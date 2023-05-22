from app import db
from app.classes.validacion import Validacion

class TipoUsuario(db.Model):
    cve_tipo_usuario = db.Column(db.Integer, primary_key=True)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        """
        Convertir el objeto del TipoUsuario a un diccionario.

        Retorno:
            dict: Diccionario que representa el TipoUsuario.
        """
        return {
            'cve_tipo_usuario': self.cve_tipo_usuario,
            'tipo_usuario': self.tipo_usuario
        }
    
    @staticmethod
    def agregar_tipousuario(tipo_usuario):
        """
        Agregar tipo de usuario a la base de datos.
        
        Entrada:
            tipo_usuario (str): tipo de usuario a agregar.
        
        Retorno exitoso:
            True: Se ha agregado exitosamente a la base de datos.
            
        Retorno fallido:
            False: No se pudo agregar a la base de datos.
        """
        try:
            tipousuario_encontrado = TipoUsuario.obtener_tipousuario_por_nombre(tipo_usuario)
            
            if not Validacion.valor_nulo(tipousuario_encontrado):
                return False
            
            nuevo_tipousuario = TipoUsuario(tipo_usuario=tipo_usuario) 
            db.session.add(nuevo_tipousuario)  
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def eliminar_tipousuario(cve_tipo_usuario):
        """
        Elimina el tipo de usuario de la base de datos.

        Entrada:
            cve_tipo_usuario (str): Clave del tipo usuario a eliminar.
            
        Retorno exitoso:
            True: Se ha eliminado correctamente.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            tipousuario_encontrado = TipoUsuario.obtener_tipousuario_por_cve(cve_tipo_usuario)

            if Validacion.valor_nulo(tipousuario_encontrado):
                return False
            
            db.session.delete(tipousuario_encontrado)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def obtener_tipousuario_por_nombre(tipo_usuario):
        """
        Obtiene tipo de usuario por su nombre.

        Argumentos:
            tipo_usuario (str): El nombre del tipo de usuario.

        Retorno exitoso:
            TipoUsuario: Objeto TipoUsuario.
        
        Retorno fallido:
            None: No se encontró o hubo un error.
        """
        try:
            tipo_usuario = TipoUsuario.query.filter_by(tipo_usuario=tipo_usuario).first()
            if not Validacion.valor_nulo(tipo_usuario):
                return tipo_usuario
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_tipousuario_por_cve(cve_tipo_usuario):
        """
        Obtiene el tipo de usuario por su clave única.

        Entrada:
            cve_tipo_usuario (int): La clave única del tipo de usuario.

        Retorno exitoso:
            TipoUsuario: Objeto TipoUsuario.
            
        Retorno fallido:
            None: No se encontró o hubo un error.
        """
        try:
            tipousuario_encontrado = TipoUsuario.query.get(cve_tipo_usuario)
            if not Validacion.valor_nulo(tipousuario_encontrado):
                return tipousuario_encontrado
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None