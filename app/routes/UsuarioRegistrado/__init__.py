from .agregar_favorito import agregar_favorito_bp
# from .crear_comentario import
# from .eliminar_comentario import
# from .eliminar_cuenta import
# from .modificar_comentario import
# from .modificar_cuenta import
from .mostrar_favoritos import mostrar_sitios_favoritos_bp
from .mostrar_sitio import mostrar_sitio_bp
from ..Sitios.mostrar_sitios import mostrar_sitios_bp
from .mostrar_recomendaciones import mostrar_recomendaciones_bp


all_blueprints = (
    agregar_favorito_bp,
    
    mostrar_sitios_bp,
    mostrar_sitios_favoritos_bp,
    mostrar_sitio_bp,
    mostrar_recomendaciones_bp
)
