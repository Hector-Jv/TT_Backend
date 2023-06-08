from .eliminar_sitio import eliminar_sitio_bp
from .generar_reglas import generar_reglas_bp
# from .inhabilitar_sitio import
# from .inhabilitar_usuario import
from .modificar_sitio import modificar_sitio_bp
# from .mostrar_usuarios import 


all_blueprints = (
    eliminar_sitio_bp,
    generar_reglas_bp,
    modificar_sitio_bp
)

