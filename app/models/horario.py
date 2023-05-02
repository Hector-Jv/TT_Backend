from app import db

class Horario(db.Model):
    cve_horario = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(100), nullable=False)
    horario_apertura = db.Column(db.Time, nullable=False)
    horario_cierre = db.Column(db.Time, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio') , nullable=False)
    
    sitio = db.relationship('Sitio', backref='horarios')