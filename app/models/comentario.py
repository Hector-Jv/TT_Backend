from datetime import datetime
from app import db

class Comentario(db.Model):
    cve_comentario = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(400), nullable=False)
    fecha_comentario = db.Column(db.DateTime, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
    
    historial = db.relationship('Historial', backref='comentarios')
    
    def __init__(self, comentario, cve_historial):
        """
        Constructor de la clase Comentario.

        Argumentos:
            comentario (str): El comentario.
            cve_historial (int): Clave del historial al que se va a asociar el comentario.
        """
        self.comentario = comentario
        self.fecha_comentario = datetime.utcnow()
        self.cve_historial = cve_historial

    def agregar_comentario(comentario):
        """
        Agregar un nuevo comentario a la base de datos.

        Argumentos:
            comentario (Comentario): La instancia de Comentario a agregar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        db.session.add(comentario)
        db.session.commit()
        return 'Comentario agregado con éxito', 200
    
    def modificar_comentario(self, comentario):
        """
        Modificar un comentario existente en la base de datos.

        Argumentos:
            comentario (str): El nuevo comentario.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        self.comentario = comentario
        db.session.commit()
        return 'Comentario modificado con éxito', 200

    def eliminar_comentario(self):
        """
        Eliminar un comentario de la base de datos.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        db.session.delete(self)
        db.session.commit()
        return 'Comentario eliminado con éxito', 200

    @staticmethod
    def consultar_comentario_por_cve(cve_comentario):
        """
        Consultar un comentario por su clave.

        Argumentos:
            cve_comentario (int): Clave del comentario.

        Retorno:
            dict, int: Diccionario con los datos del comentario y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        comentario = Comentario.query.get(cve_comentario)
        if comentario:
            return {
                'comentario': comentario.comentario,
                'fecha_comentario': comentario.fecha_comentario,
                'cve_historial': comentario.cve_historial
            }, 200
        return 'Comentario no encontrado', 404

    @staticmethod
    def consultar_comentarios_por_historial(cve_historial):
        """
        Consultar todos los comentarios asociados a un historial.

        Argumentos:
            cve_historial (int): Clave del historial.

        Retorno:
            list, int: Lista de diccionarios con los datos de los comentarios y código de estado HTTP, o mensaje de error y código de estado HTTP.
        """
        comentarios = Comentario.query.filter_by(cve_historial=cve_historial).all()
        if comentarios:
            return [{
                'cve_comentario': comentario.cve_comentario,
                'comentario': comentario.comentario,
                'fecha_comentario': comentario.fecha_comentario,
                'cve_historial': comentario.cve_historial
            } for comentario in comentarios], 200
        return 'No se encontraron comentarios para ese historial', 404
