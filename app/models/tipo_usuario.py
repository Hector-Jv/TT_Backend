from app import db

class TipoUsuario(db.Model):
    """
    Modelo para tipos de usuarios en la aplicación.

    Atributos:
        cve_tipo_usuario (int): Clave única para cada tipo de usuario.
        tipo_usuario (str): Nombre del tipo de usuario.
    """
    
    cve_tipo_usuario = db.Column(db.Integer, primary_key=True)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    
    def agregar_tipo_usuario(self):
        """
        Agrega el tipo de usuario actual a la base de datos.

        Retorno:
            str: Mensaje indicando que el tipo de usuario se guardó con éxito.
            int: Código de estado HTTP 200.
        """
        db.session.add(self)
        db.session.commit()
        return 'Tipo usuario guardado', 200
    
    def eliminar_tipo_usuario(self):
        """
        Elimina el tipo de usuario actual de la base de datos.

        Retorno:
            str: Mensaje indicando que el tipo de usuario se eliminó con éxito.
            int: Código de estado HTTP 200.
        """
        db.session.delete(self)
        db.session.commit()
        return 'Tipo usuario eliminado.', 200
    
    @staticmethod
    def obtener_tipo_usuario(cve_tipo_usuario):
        """
        Obtiene un tipo de usuario por su clave única.

        Argumentos:
            cve_tipo_usuario (int): La clave única del tipo de usuario a obtener.

        Retorno:
            TipoUsuario: El objeto TipoUsuario correspondiente a la clave proporcionada, o None si no se encuentra.
        """
        tipo_usuario = TipoUsuario.query.get(cve_tipo_usuario)
        if tipo_usuario is None:
            return None
        return tipo_usuario
    
    @staticmethod
    def obtener_id_tipo_usuario(tipo):
        """
        Obtiene la clave única de un tipo de usuario por su nombre.

        Argumentos:
            tipo (str): El nombre del tipo de usuario.

        Retorno:
            int: La clave única del tipo de usuario, o None si no se encuentra.
        """
        tipo_usuario = TipoUsuario.query.filter_by(tipo_usuario=tipo).first()
        if tipo_usuario is None:
            return None
        return tipo_usuario.cve_tipo_usuario
    
    @staticmethod
    def obtener_nombre_tipo_usuario(id):
        """
        Obtiene el nombre de un tipo de usuario por su clave única.

        Argumentos:
            id (int): La clave única del tipo de usuario.

        Retorno:
            str: El nombre del tipo de usuario, o None si no se encuentra.
        """
        tipo_usuario = TipoUsuario.query.get(id)
        if tipo_usuario is None:
            return None
        return tipo_usuario.tipo_usuario