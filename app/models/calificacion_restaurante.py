from app import db

class CalificacionRestaurante(db.Model):
    cve_calificacion = db.Column(db.Integer, db.ForeignKey('calificacion.cve_calificacion'), primary_key=True)
    calidad_servicio = db.Column(db.Float, nullable=False)
    sabor = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    limpieza = db.Column(db.Float, nullable=False)

    def __init__(self, calidad_servicio, sabor, costo, limpieza):
        """
        Inicializa una nueva calificación para un restaurante.

        Argumentos:
            calidad_servicio (float): Calificación para la calidad del servicio.
            sabor (float): Calificación para el sabor.
            costo (float): Calificación para el costo.
            limpieza (float): Calificación para la limpieza.
        """
        self.calidad_servicio = calidad_servicio
        self.sabor = sabor
        self.costo = costo
        self.limpieza = limpieza

    def modificar_calificacion(self, calidad_servicio=None, sabor=None, costo=None, limpieza=None):
        """
        Modifica la calificación del restaurante. Solo los argumentos que no sean None serán modificados.
        
        Argumentos:
            calidad_servicio (float, optional): Nueva calificación para la calidad del servicio. Si es None, no se modificará.
            sabor (float, optional): Nueva calificación para el sabor. Si es None, no se modificará.
            costo (float, optional): Nueva calificación para el costo. Si es None, no se modificará.
            limpieza (float, optional): Nueva calificación para la limpieza. Si es None, no se modificará.
        """
        if calidad_servicio is not None:
            self.calidad_servicio = calidad_servicio
        if sabor is not None:
            self.sabor = sabor
        if costo is not None:
            self.costo = costo
        if limpieza is not None:
            self.limpieza = limpieza
        db.session.commit()
        
    @classmethod
    def eliminar_calificacion(cls, cve_calificacion):
        """
        Método para eliminar una calificación de un restaurante.

        Argumentos:
            cve_calificacion (int): Clave de la calificación a eliminar.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        calificacion = cls.query.get(cve_calificacion)
        if calificacion:
            db.session.delete(calificacion)
            db.session.commit()
            return {'message': 'Calificación eliminada con éxito.'}, 200
        return 'Calificación no encontrada', 404

    @classmethod
    def consultar_calificacion(cls, cve_calificacion):
        """
        Consulta la calificación de un restaurante.

        Argumentos:
            cve_calificacion (int): Clave de la calificación a consultar.

        Retorno:
            dict, int: Diccionario con los datos de la calificación y código de estado HTTP, o mensaje de error y código de estado en caso de fallo.
        """
        calificacion = cls.query.get(cve_calificacion)
        if calificacion:
            return {
                'cve_calificacion': calificacion.cve_calificacion,
                'calidad_servicio': calificacion.calidad_servicio,
                'sabor': calificacion.sabor,
                'costo': calificacion.costo,
                'limpieza': calificacion.limpieza
            }, 200
        else:
            return 'Calificación no encontrada', 404
