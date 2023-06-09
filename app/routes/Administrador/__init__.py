from .eliminar_sitio import eliminar_sitio_bp
from .generar_reglas import generar_reglas_bp
from .inhabilitar_sitio import inhabilitar_sitio_bp
from .modificar_sitio import modificar_sitio_bp
from .mostrar_usuarios import mostrar_usuarios_bp
from .mostrar_usuario import mostrar_usuario_bp
from .inhabilitar_usuario import inhabilitar_usuario_bp


all_blueprints = (
    eliminar_sitio_bp,
    generar_reglas_bp,
    inhabilitar_sitio_bp,
    modificar_sitio_bp,
    mostrar_usuarios_bp,
    mostrar_usuario_bp,
    inhabilitar_usuario_bp
)

