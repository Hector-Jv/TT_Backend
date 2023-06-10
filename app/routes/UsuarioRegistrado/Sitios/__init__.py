from .agregar_favorito import agregar_favorito_bp
from .mostrar_recomendaciones import mostrar_recomendaciones_bp
from .mostrar_favoritos import mostrar_favoritos_bp
from .agregar_historial import agregar_historial_bp

all_blueprints_sitios = (
    agregar_favorito_bp,
    mostrar_recomendaciones_bp,
    mostrar_favoritos_bp,
    agregar_historial_bp
)