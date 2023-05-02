from app import db

class Comentario(db.Model):
    cve_comentario = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(400), nullable=False)
    fecha_comentario = db.Column(db.DateTime, nullable=False)
    cve_historial = db.Column(db.Integer, db.ForeignKey('historial.cve_historial'), nullable=False)
    
    historial = db.relationship('Historial', backref='comentarios')