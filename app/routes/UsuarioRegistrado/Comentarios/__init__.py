from .crear_comentario import crear_comentario_bp
from.mostrar_reseñas import mostrar_reseña_bp
from .eliminar_comentario import eliminar_comentario_bp
#from .modificar_comentario import modificar_comentario_bp


all_blueprints_comentarios = (
    crear_comentario_bp,
    mostrar_reseña_bp,
    eliminar_comentario_bp,
    #modificar_comentario_bp
)