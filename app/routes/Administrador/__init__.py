from .eliminar_sitio import eliminar_sitio_bp
from .generar_reglas import generar_reglas_bp
from .inhabilitar_sitio import inhabilitar_sitio_bp
from .modificar_sitio import modificar_sitio_bp


all_blueprints = (
    eliminar_sitio_bp,
    generar_reglas_bp,
    inhabilitar_sitio_bp,
    modificar_sitio_bp
)

