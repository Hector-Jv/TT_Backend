from app import db

class FotoComentario(db.Model):
    cve_foto_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    link_imagen = db.Column(db.String(200), nullable=False)
    nombre_imagen = db.Column(db.String(100), nullable=True)
    nombre_autor = db.Column(db.String(300), nullable=True)
    cve_comentario = db.Column(db.Integer, db.ForeignKey('comentario.cve_comentario'), nullable=False)
    
    def __init__(self, link_imagen: str, cve_comentario: int, nombre_imagen: str = '', nombre_autor: str = ''):
        self.link_imagen = link_imagen
        self.cve_comentario = cve_comentario
        self.nombre_imagen = nombre_imagen
        self.nombre_autor = nombre_autor
        
    