import datetime
from app import db

from app.classes.validacion import Validacion

class Comentario(db.Model):
    cve_comentario = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(400), nullable=False)
    fecha_comentario = db.Column(db.DateTime, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
    
    historial = db.relationship('Historial', backref='comentarios')
    
    def to_dict(self):
        """
        Convertir el objeto del Comentario a un diccionario.

        Retorno:
            dict: Diccionario que representa el comentario.
        """
        return {
            'cve_comentario': self.cve_comentario,
            'comentario': self.comentario,
            'fecha_comentario': str(self.fecha_comentario),
            'cve_historial': self.cve_historial
        }
    
    @staticmethod
    def agregar_comentario(comentario, cve_historial):
        """
        Agregar comentario a sitio de interés.
        
        Entrada:
            comentario (str): El comentario.
            cve_historial (int): Clave del historial al que se va a asociar el comentario.
            
        Retorno exitoso:
            True: Se a agregado exitosamente el comentario a la base de datos.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            historial_encontrado = Comentario.obtener_comentario_por_historial(cve_historial)
            
            if not Validacion.valor_nulo(historial_encontrado):
                return False
            
            nuevo_comentario = Comentario(
                comentario = comentario,
                fecha_comentario = datetime.utcnow(),
                cve_historial = cve_historial
            )
            
            db.session.add(nuevo_comentario)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def modificar_comentario(cve_comentario, comentario):
        """
        Modifica un comentario existente en la base de datos.

        Entrada:
            cve_comentario (int): Clave de comentario
            comentario (str): El nuevo comentario.

        Retorno exitoso:
            True: Se ha modificado el comentario con exito.
            
        Retorno fallido:
            False: Ha habido un error.
        """
        try:
            comentario_encontrado = Comentario.obtener_comentario_por_cve(cve_comentario)
            
            if Validacion.valor_nulo(comentario_encontrado):
                return False
            
            comentario_encontrado.comentario = comentario
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def eliminar_comentario(cve_comentario):
        """
        Eliminar un comentario de la base de datos.

        Retorno exitoso:
            True: Se pudo eliminar con exito el comentario de la base de datos.
            
        Retorno fallido:
            False: Hubo un error o no se encontraba el comentario a eliminar.
        """
        try:
            comentario_encontrado = Comentario.obtener_comentario_por_cve(cve_comentario)
            
            if not Validacion.valor_nulo(comentario_encontrado):
                db.session.delete(comentario_encontrado)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_comentario_por_cve(cve_comentario):
        """
        Obtener un comentario por su clave..

        Entrada:
            cve_comentario (int): Clave del comentario.

        Retorno exitoso:
            Comentario: Instancia de tipo Comentario.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron.
        """
        try:
            comentario_encontrado = Comentario.query.get(cve_comentario)
            
            if not Validacion.valor_nulo(comentario_encontrado):
                return comentario_encontrado
            else:
                return None
        except Exception as e:
            return None

    ## Se esta trabajando como 1 a 1, pero se puede cambiar a 1 a n.
    @staticmethod
    def obtener_comentario_por_historial(cve_historial):
        """
        Obtiener comentario de un historial.

        Entrada:
            cve_historial (int): Clave del historial.

        Retorno exitoso:
            Comentario: Instancia de tipo Comentario.
            
        Retorno fallido:
            None: Hubo un error o no se encontraron.
        """
        try:
            comentario_encontrado = Comentario.query.filter_by(cve_historial=cve_historial).first()
            
            if not Validacion.valor_nulo(comentario_encontrado):
                return comentario_encontrado
            else:
                return None
        except Exception as e:
            return None
