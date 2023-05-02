from app import db
from .calificacion import Calificacion

class CalificacionRestaurante(Calificacion):

    __mapper_args__ = {
        'polymorphic_identity': 'calificacion_restaurante',
    }

    @property
    def atencion(self):
        return self.calificaciones_especificas.get('atencion')

    @property
    def sabor(self):
        return self.calificaciones_especificas.get('sabor')

    @property
    def costo(self):
        return self.calificaciones_especificas.get('costo')

    @property
    def limpieza(self):
        return self.calificaciones_especificas.get('limpieza')
