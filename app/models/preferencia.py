from app import db
from .usuario import Usuario
from .etiqueta import Etiqueta
from app.classes.validacion import Validacion

class Preferencia(db.Model):
    correo_usuario = db.Column(db.String(100), primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['correo_usuario'],
            ['usuario.correo_usuario'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )
    
    def to_dict(self):
        """
        Convertir el objeto Preferencia a un diccionario.

        Retorno:
            dict: Diccionario que representa el Preferencia.
        """
        return {
            'correo_usuario': self.correo_usuario,
            'cve_etiqueta': self.cve_etiqueta
        }
        
    @staticmethod
    def agregar_preferencia(correo_usuario, cve_etiqueta):
        """
        Agrega una nueva preferencia de usuario en la base de datos.
        
        Entrada:
            correo_usuario (str): Clave de usuario.
            cve_etiqueta (int): Clave de la etiqueta.
            
        Retorno exitoso:
            True: Se ha agregado correctamente a la base de datos.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            relacion_encontrada = Preferencia.obtener_relacion_preferencia(correo_usuario=correo_usuario, cve_etiqueta=cve_etiqueta)
            
            if not Validacion.valor_nulo(relacion_encontrada):
                return False
            
            nueva_relacion = Preferencia(
                correo_usuario=correo_usuario, 
                cve_etiqueta=cve_etiqueta
            )
            db.session.add(nueva_relacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def eliminar_preferencia(correo_usuario, cve_etiqueta):
        """
        Eliminar una relación de la base de datos.
        
        Entrada:
            correo_usuario (str): Correo de usuario
            cve_etiqueta (int): Clave de etiqueta.
        
        Retorno exitoso:
            True: Se elimino de manera correcta.
        
        Retorno fallido:
            False: Hubo un error
        """
        try:
            relacion_encontrada = Preferencia.obtener_relacion_preferencia(correo_usuario=correo_usuario, cve_etiqueta=cve_etiqueta)

            if not Validacion.valor_nulo(relacion_encontrada):
                db.session.delete(relacion_encontrada)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_preferencias_por_correo(correo_usuario):
        """
        Obtener todas las relaciones que tengan el mismo correo de usuario.

        Entrada:
            correo_usuario (str): Correo de usuario.
            
        Retorno exitoso:
            list: Lista de instancias de tipo Preferencia.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron relaciones.
        """
        try:
            relaciones_encontradas = Preferencia.query.filter_by(correo_usuario=correo_usuario).all()
            
            if not Validacion.valor_nulo(relaciones_encontradas):
                return relaciones_encontradas
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_preferencias_por_cveetiqueta(cve_etiqueta):
        """
        Obtener todas las relaciones que tengan la misma clave etiqueta.

        Entrada:
            cve_etiqueta (int): Clave de etiqueta.
            
        Retorno exitoso:
            list: Lista de instancias de tipo Preferencia.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron relaciones.
        """
        try:
            relaciones_encontradas = Preferencia.query.filter_by(cve_etiqueta=cve_etiqueta).all()
            
            if not Validacion.valor_nulo(relaciones_encontradas):
                return relaciones_encontradas
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        
    @staticmethod
    def obtener_relacion_preferencia(correo_usuario, cve_etiqueta):
        """
        Verifica si hay una relación entre un usuario y una etiqueta.

        Entrada:
            correo_usuario (str): Correo de usuario
            cve_etiqueta (int): Clave de la etiqueta a consultar.

        Retorno exitoso:
            Preferencia: Instancia Preferencia.
        
        Retorno fallido:
            None: No existe una relación.
        """
        try:
            relacion_encontrada = Preferencia.query.filter_by(correo_usuario=correo_usuario, cve_etiqueta=cve_etiqueta).first()
            if not Validacion.valor_nulo(relacion_encontrada):
                return relacion_encontrada
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        
