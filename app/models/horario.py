from app import db

class Horario(db.Model):
    cve_horario = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(100), nullable=False)
    horario_apertura = db.Column(db.Time, nullable=False)
    horario_cierre = db.Column(db.Time, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio') , nullable=False)
    
    sitio = db.relationship('Sitio', backref='horarios')

    def __init__(self, dia, horario_apertura, horario_cierre, cve_sitio):
        """
        Método para crear una nueva instancia de Horario.

        Argumentos:
            dia (str): Día de la semana.
            horario_apertura (Time): Hora de apertura del sitio.
            horario_cierre (Time): Hora de cierre del sitio.
            cve_sitio (int): Clave del sitio al que pertenece este horario.
        """
        self.dia = dia
        self.horario_apertura = horario_apertura
        self.horario_cierre = horario_cierre
        self.cve_sitio = cve_sitio

    def modificar_horario(self, dia, horario_apertura, horario_cierre):
        """
        Método para modificar un horario existente.

        Argumentos:
            dia (str): Nuevo día de la semana.
            horario_apertura (Time): Nueva hora de apertura del sitio.
            horario_cierre (Time): Nueva hora de cierre del sitio.
        """
        self.dia = dia
        self.horario_apertura = horario_apertura
        self.horario_cierre = horario_cierre
        db.session.commit()

    @staticmethod
    def consultar_horario(cve_horario):
        """
        Método para consultar un horario específico por su clave.

        Argumentos:
            cve_horario (int): Clave del horario a consultar.

        Retorno:
            dict, int: Diccionario con la información del horario y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        horario = Horario.query.get(cve_horario)
        if horario:
            return {
                'cve_horario': horario.cve_horario,
                'dia': horario.dia,
                'horario_apertura': str(horario.horario_apertura),
                'horario_cierre': str(horario.horario_cierre),
                'cve_sitio': horario.cve_sitio
            }, 200
        return 'Horario no encontrado', 404

    @staticmethod
    def consultar_horarios_por_sitio(cve_sitio):
        """
        Método para consultar todos los horarios de un sitio específico.

        Argumentos:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno:
            list, int: Lista de diccionarios con la información de los horarios y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        horarios = Horario.query.filter_by(cve_sitio=cve_sitio).all()
        if horarios:
            return [{
                'cve_horario': horario.cve_horario,
                'dia': horario.dia,
                'horario_apertura': str(horario.horario_apertura),
                'horario_cierre': str(horario.horario_cierre),
                'cve_sitio': horario.cve_sitio
            } for horario in horarios], 200
        return 'No se encontraron horarios para este sitio', 404

    @staticmethod
    def eliminar_horario(cve_horario):
        """
        Método para eliminar un horario específico.

        Argumentos:
            cve_horario (int): Clave del horario a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        horario = Horario.query.get(cve_horario)
        if horario:
            db.session.delete(horario)
            db.session.commit()
            return {'message': 'Horario eliminado exitosamente.'}, 200
        return 'Horario no encontrado', 404