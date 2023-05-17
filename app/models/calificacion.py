from app import db
from sqlalchemy import func

class Calificacion(db.Model):
    """
    Modelo que representa la tabla Calificación en la base de datos.
    """
    cve_calificacion = db.Column(db.Integer, primary_key=True)
    calificacion_general = db.Column(db.Float, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
    
    # Relaciones uno a uno con las tablas de calificaciones específicas
    calificacion_hotel = db.relationship('CalificacionHotel', backref='calificacion', uselist=False)
    calificacion_restaurante = db.relationship('CalificacionRestaurante', backref='calificacion', uselist=False)

    def __init__(self, cve_historial, calificacion_general):
        """
        Crea una nueva instancia de Calificacion.
        
        Argumentos:
            cve_historial (int): Clave del historial asociado a esta calificación.
            calificacion_general (float): Calificación general asignada.
        """
        self.cve_historial = cve_historial
        self.calificacion_general = calificacion_general

    def modificar_calificacion(self, calificacion_general):
        """
        Modifica la calificación general de la instancia actual.
        
        Argumentos:
            calificacion_general (float): Nueva calificación general a asignar.
        """
        self.calificacion_general = calificacion_general
        db.session.commit()

    @staticmethod
    def consultar_calificacion(cve_calificacion):
        """
        Consulta una calificación por su clave.

        Argumentos:
            cve_calificacion (int): Clave de la calificación a consultar.

        Retorno:
            dict: Diccionario con la información de la calificación si se encuentra, 
                  y un mensaje de error si no se encuentra.
        """
        calificacion = Calificacion.query.get(cve_calificacion)
        if calificacion:
            return {
                'cve_calificacion': calificacion.cve_calificacion,
                'calificacion_general': calificacion.calificacion_general,
                'cve_historial': calificacion.cve_historial,
            }, 200
        return 'Calificacion no encontrada', 404

    @staticmethod
    def consultar_calificaciones_por_rango(rango_bajo, rango_alto):
        """
        Consulta todas las calificaciones que se encuentren dentro de un rango específico.

        Argumentos:
            rango_bajo (float): Límite inferior del rango de calificaciones a consultar.
            rango_alto (float): Límite superior del rango de calificaciones a consultar.

        Retorno:
            list: Lista de diccionarios con la información de las calificaciones si se encuentran, 
                  y un mensaje de error si no se encuentran.
        """
        calificaciones = Calificacion.query.filter(Calificacion.calificacion_general.between(rango_bajo, rango_alto)).all()
        if calificaciones:
            return [{
                'cve_calificacion': calificacion.cve_calificacion,
                'calificacion_general': calificacion.calificacion_general,
                'cve_historial': calificacion.cve_historial,
            } for calificacion in calificaciones], 200
        return 'No se encontraron calificaciones dentro del rango especificado', 404

    @staticmethod
    def promedio_calificaciones_por_historial(cve_historial):
        """
        Calcula el promedio de las calificaciones asociadas a un historial específico.

        Argumentos:
            cve_historial (int): Clave del historial a consultar.

        Retorno:
            dict: Diccionario con el promedio de las calificaciones si se encuentran, 
                  y un mensaje de error si no se encuentran.
        """
        promedio = db.session.query(func.avg(Calificacion.calificacion_general)).filter(
            Calificacion.cve_historial == cve_historial).scalar()
        return {'promedio_calificaciones': promedio} if promedio else 'No se encontraron calificaciones para este historial', 404
