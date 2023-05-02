from app import db
from .calificacion import Calificacion

class CalificacionHotel(Calificacion):
    
    __mapper_args__ = {
        'polymorphic_identity': 'calificacion_hotel',
    }

    @property
    def atencion(self):
        return self.calificaciones_especificas.get('atencion')

    @property
    def limpieza(self):
        return self.calificaciones_especificas.get('limpieza')

    @property
    def costo(self):
        return self.calificaciones_especificas.get('costo')