from .iniciar_sesion import iniciar_sesion_bp
from .registrar_usuario import registrar_usuario_bp


all_blueprints = (
    iniciar_sesion_bp, 
    registrar_usuario_bp
)