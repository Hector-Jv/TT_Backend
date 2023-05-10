from app import db
import re # Uso de expresiones regulares.

def datos_necesarios(*datos: tuple):
    """ Valida que los datos tengan algún contenido o valor.
    """
    for dato in datos:
        if not dato:
            return False
    return True

def formato_correo(correo):
    correo_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(correo_regex, correo):
        return True
    return False

def formato_contrasena(contrasena):
    """ Verifica que la contraseña cumpla con el formato correcto (al menos 8 caracteres, una letra mayúscula, un número y un carácter especial)
    """
    contrasena_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$'
    if re.match(contrasena_regex, contrasena):
        return True
    return False


