from flask import Blueprint, jsonify, request
from app import db
from app.models import Usuario, TipoUsuario
from app.classes.validacion import Validacion
from app.classes.imagen import Imagen
import os


registro_bp = Blueprint('registro', __name__)


@registro_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró la imagen"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "El nombre de la imagen está vacío"}), 400

    # Cambia 'uploads' al nombre de la carpeta donde deseas guardar las imágenes
    folder_path = 'uploads'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image.save(os.path.join(folder_path, image.filename))
    return jsonify({"message": "Imagen guardada correctamente"}), 200



@registro_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    
    ## Datos necesarios ##
    data = request.get_json()
    correo = data.get('correo')
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    ## Validaciones ##

    if not Validacion.datos_necesarios(correo, usuario, contrasena):
        return jsonify({"error": "Hacen falta datos."}), 400
    
    if not Validacion.formato_correo(correo):
        return jsonify({"error": "El correo ingresado no es válido."}), 400

    if not Validacion.formato_contrasena(contrasena):
        return jsonify({"error": "La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial."}), 400

    usuario_encontrado = Usuario.consulta_por_correo(correo)
    
    if not Validacion.valor_nulo(usuario_encontrado):
        return jsonify({"error": "Ya existe el correo ingresado."}), 404
    
    usuario_encontrado = Usuario.consulta_por_usuario(usuario)
    
    if not Validacion.valor_nulo(usuario_encontrado):
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