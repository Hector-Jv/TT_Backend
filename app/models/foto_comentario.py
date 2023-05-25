from app import db
from app.classes.validacion import Validacion
from .comentario import Comentario

class FotoComentario(db.Model):
    cve_foto_comentario = db.Column(db.Integer, autoincrement=True, nullable=False)
    nombre_imagen = db.Column(db.String(400), nullable=False)
    link_imagen = db.Column(db.String(400), nullable=False)
    nombre_autor = db.Column(db.String(400), nullable=False)
    cve_comentario = db.Column(db.Integer, db.ForeignKey('comentario.cve_comentario'), nullable=False)
    
    comentario = db.relationship('Comentario', backref='fotos_comentario')

    __table_args__ = (
        db.PrimaryKeyConstraint('cve_foto_comentario', 'cve_comentario'),
    )
    
    def to_dict(self):
        """
        Convertir el objeto FotoComentario a un diccionario.

        Retorno:
            dict: Diccionario que representa FotoComentario.
        """
        return {
            'cve_foto_comentario': self.cve_foto_comentario,
            'nombre_imagen': self.nombre_imagen,
            'cve_comentario': self.cve_comentario
        }
    
    @staticmethod
    def guardar_imagen(nombre_imagen, cve_comentario):
        """
        Guarda una imagen asociada a un comentario en la base de datos.

        Entrada:
            nombre_imagen (str): Nombre de la imagen.
            cve_comentario (int): La clave del comentario asociado a la imagen.

        Retorno exitoso:
            True: Se guardo de manera correcta.
            
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            comentario_encontrado = Comentario.obtener_comentario_por_cve(cve_comentario)
            
            if Validacion.valor_nulo(comentario_encontrado):
                return False
            
            nuevo_fotocomentario = FotoComentario(
                nombre_imagen = nombre_imagen,
                cve_comentario = cve_comentario
            )
            db.session.add(nuevo_fotocomentario)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def eliminar_foto(cve_foto_comentario):
        """
        Elimina una foto específica.

        Entrada:
            cve_foto_comentario (int): La clave de la foto a eliminar.

        Retorno exitoso:
            True: Fue eliminado correctamente.
        
        Retorno fallido:
            False: Hubo un error o no existe.
        """
        try:
            fotocomentario_encontrado = FotoComentario.obtener_fotocomentario_por_cve(cve_foto_comentario)
            
            if Validacion.valor_nulo(fotocomentario_encontrado):
                return False
            
            db.session.delete(fotocomentario_encontrado)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
    
    @staticmethod
    def obtener_fotos_por_comentario(cve_comentario):
        """
        Obtiene las fotos asociadas a un comentario en particular.

        Entrada:
            cve_comentario (int): La clave del comentario asociado a las imágenes.
        
        Retorno exitoso:
            list: Lista con instancia de tipo FotoComentario.
            
        Retorno fallido:
            []: Hubo un error o está vacía.
        """
        try: 
            fotos_comentario = FotoComentario.query.filter_by(cve_comentario=cve_comentario).all()

            if Validacion.valor_nulo(fotos_comentario):
                return fotos_comentario
            else:
                return []
        except Exception as e:
            print("Hubo un error: ", e)
            return []
    
    @staticmethod
    def obtener_fotocomentario_por_cve(cve_foto_comentario):
        """
        Obtiene fotocomentario por clave.
        
        Entrada: 
            cve_foto_comentario (int): Clave de FotoComentario.
            
        Retorno exitoso:
            FotoComentario: Instancia de tipo FotoComentario.
        
        Retorno fallido:
            None: Hubo un error o no existe.
        """
        try:
            fotocomentario_encontrado = FotoComentario.query.get(cve_foto_comentario)
            
            if Validacion.valor_nulo(fotocomentario_encontrado):
                return None
            
            return fotocomentario_encontrado
            
        except Exception as e:
            print("Hubo un error: ", e)
            return None