from app import db

class Colonia(db.Model):
    cve_colonia = db.Column(db.Integer, primary_key=True)
    nombre_colonia = db.Column(db.String(400), nullable=False)
    cve_delegacion = db.Column(db.Integer, db.ForeignKey('delegacion.cve_delegacion') , nullable=False)
    
    delegacion = db.relationship('Delegacion', backref='colonias')

    