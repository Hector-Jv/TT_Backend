from .datos_para_crear_sitio import datos_para_crear_sitio_bp
from .eliminar_sitio import eliminar_sitio_bp
from .generar_reglas import generar_reglas_bp
# from .inhabilitar_sitio import
# from .inhabilitar_usuario import
from .modificar_sitio import modificar_sitio_bp
# from .mostrar_usuarios import 


all_blueprints = (
    datos_para_crear_sitio_bp,
    eliminar_sitio_bp,
    generar_reglas_bp,
    modificar_sitio_bp
)

