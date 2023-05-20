import re # Uso de expresiones regulares.

class Validacion():
        
    @staticmethod
    def datos_necesarios(*datos):
        """ 
        Valida que los datos tengan algún contenido o valor.
        
        Retorno exitoso:
            True: Contienen todos los datos algún valor.
            
        Retorno fallido:
            False: Hay uno o más datos que no tienen valor asignado.
        """
        for dato in datos:
            if not dato:
                return False
        return True

    @staticmethod
    def formato_correo(correo):
        """
        Valida el formato del correo del usuario.
        
        Retorno exitoso:
            True: Si cumple con el formato.
        
        Retorno fallido:
            False: No cumple con el formato.
        """
        correo_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(correo_regex, correo):
            return True
        return False

    @staticmethod
    def formato_contrasena(contrasena):
        """ 
        Verifica que la contraseña cumpla con el formato correcto (al menos 8 caracteres, una letra mayúscula, un número y un carácter especial)
        
        Retorno exitoso:
            True: Si cumple con el formato.
        
        Retorno fallido:
            False: No cumple con el formato.
        """
        contrasena_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$'
        if re.match(contrasena_regex, contrasena):
            return True
        return False
    
    @staticmethod
    def valor_nulo(dato):
        """
        Verifica que el dato ingresado sea nulo.
        
        Retorno Exitoso:
            True: El dato es nulo.
        
        Retorno Fallido:
            False: El dato no es nulo.
        """
        if dato is None:
            return True
        else:
            return False