from app import db

"""Insercion
nueva_calificacion_hotel = CalificacionHotel(
    cve_historial=1,
    calificacion_general=4.0,
    calificaciones_especificas={
        'atencion': 4.5,
        'limpieza': 4.0,
        'costo': 3.5
    },
    tipo='calificacion_hotel'
)
db.session.add(nueva_calificacion_hotel)
db.session.commit()
"""



class Calificacion(db.Model):
    cve_calificacion = db.Column(db.Integer, primary_key=True)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
    calificacion_general = db.Column(db.Float(2), nullable=False)
    calificaciones_especificas = db.Column(db.JSON, nullable=True) # Almacena las calificaciones específicas en JSON
    tipo = db.Column(db.String(50)) # Funciona como un discriminador.

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'calificacion',
    }

    historial = db.relationship('Historial', backref='calificaciones')
