from .sitios_ruta import sitio_bp
"""
sitio_bp
    @sitio_bp.route('/')
    @sitio_bp.route('/inicio', methods=["GET"])
    @sitio_bp.route('/sitios', methods=["GET"])
    @sitio_bp.route('/sitios/filtros', methods=["GET"])
    @sitio_bp.route('/sitios/<cve_sitio>', methods=["GET"])
    @sitio_bp.route('/sitio_favorito', methods=["POST"])
"""

from .login_routes import login_bp
"""
login_bp
    @login_bp.route('/login', methods=['POST'])
"""

from .registro_routes import registro_bp
"""
registro_bp
    @registro_bp.route('/registro', methods=['POST'])
"""

from .usuario_routes import usuario_bp
"""
usuario_bp
    @usuario_bp.route('/usuario', methods=['GET']) @jwt_required()
    @usuario_bp.route('/admin', methods=['GET']) @jwt_required()
"""

"""
from .sitio_routes import sitio_bp

    @sitio_bp.route('/imagen', methods=['POST'])
    @sitio_bp.route('/imagenes_sitio/<int:cve_sitio>')
    @sitio_bp.route('/data/sitios/<path:filename>')
    @sitio_bp.route('/sitios', methods=['GET'])
    @sitio_bp.route('/sitio', methods=['POST'])
    @sitio_bp.route('/sitio', methods=['DELETE'])
    @sitio_bp.route('/sitio', methods=['PUT'])
"""