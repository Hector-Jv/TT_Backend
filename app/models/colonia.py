from app import db

class Colonia(db.Model):
    cve_colonia = db.Column(db.Integer, primary_key=True)
    nombre_colonia = db.Column(db.String(400), nullable=False)
    cve_delegacion = db.Column(db.Integer, db.ForeignKey('delegacion.cve_delegacion') , nullable=False)
    
    delegacion = db.relationship('Delegacion', backref='colonias')

    def guardar(self):
        db.session.add(self)
        db.session.commit()
        return 'Colonia guardada', 200
        
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
        return 'Colonia eliminada.', 201
        
    @classmethod
    def obtener_colonia_por_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def obtener_colonias(cls):
        return cls.query.all()
    
    @classmethod
    def obtener_colonia_por_nombre(cls, nombre):
        return cls.query.filter_by(nombre_colonia=nombre).first()
    
    @classmethod
    def obtener_colonias_de_delegacion(cls, id_delegacion):
        return cls.query.filter_by(cve_delegacion=id_delegacion).all()