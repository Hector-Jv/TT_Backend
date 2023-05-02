from app import db

class FotoComentario(db.Model):
    cve_foto_comentario = db.Column(db.Integer, primary_key=True)
    foto_comentario = db.Column(db.String(400), nullable=False)
    cve_comentario = db.Column(db.Integer, db.ForeignKey('comentario.cve_comentario'), nullable=False)
    
    comentario = db.relationship('Comentario', backref='fotos_comentario')