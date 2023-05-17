from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, TipoUsuario
from app.utils.validaciones import datos_necesarios, formato_contrasena, formato_correo


registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    
    # Datos recibidos del usuario.
    data = request.get_json()

    # Se extraen los datos recibidos del usuario.
    correo = data.get('correo')
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    foto_usuario = data.get('foto_usuario', None)

    # Se verifica que hayan entregado los datos necesarios.
    if not datos_necesarios(correo, usuario, contrasena):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    # Se verifica que el correo tenga el formato correcto.
    if not formato_correo(correo):
        return jsonify({"error": "El correo ingresado no es válido."}), 400

    # Se verifica que la contraseña cumpla con el formato correcto.
    if not formato_contrasena(contrasena):
        return jsonify({"error": "La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial."}), 400

    # Busca si el correo ingresado se encuentra registrado.
    existe_correo = Usuario.query.filter_by(correo_usuario=correo).first()
    
    # Se verifica que no haya una cuenta registrada con el mismo correo.
    if existe_correo is not None:
        return jsonify({"error": "Ya existe el correo ingresado."}), 404
    
    # Busca si el usuario ingresado se encuentra registrado.
    existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

    # Se verifica que no haya una cuenta registrada con el mismo usuario.
    if existe_usuario is not None:
        return jsonify({"error": "Ya existe el usuario ingresado."}), 404

    # Busca el tipo de usuario que pertenece el usuario.
    tipo_usuario = TipoUsuario.query.filter_by(tipo_usuario="Usuario registrado").first()    
    
    # Se manda a llamar el modelo Usuario para crear un nuevo usuario.
    nuevo_usuario = Usuario(
        correo_usuario=correo, 
        usuario=usuario, 
        contrasena=contrasena, 
        foto=foto_usuario, 
        cve_tipo_usuario=tipo_usuario.cve_tipo_usuario
    )
    
    # Se añade el usuario a la sesión.
    db.session.add(nuevo_usuario)
    
    # Se confirma y se aplican los cambios realizados en la base de datos.
    db.session.commit()
    
    # Si todo sale bien, regresa un json con el nombre de usuario (se va a modificar)
    return jsonify({"usuario": nuevo_usuario.usuario, "correo_usuario": correo, "message": "Usuario creado con éxito"}), 201