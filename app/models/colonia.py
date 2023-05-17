from app import db

class Colonia(db.Model):
    cve_colonia = db.Column(db.Integer, primary_key=True)
    nombre_colonia = db.Column(db.String(400), nullable=False)
    cve_delegacion = db.Column(db.Integer, db.ForeignKey('delegacion.cve_delegacion') , nullable=False)
    
    delegacion = db.relationship('Delegacion', backref='colonias')
    
    def to_dict(self):
        """
        Método para convertir el objeto de la colonia a un diccionario.

        Retorno:
            dict: Diccionario que representa la colonia.
        """
        return {
            'cve_colonia': self.cve_colonia,
            'nombre_colonia': self.nombre_colonia,
            'cve_delegacion': self.cve_delegacion
        }

    def guardar(self):
        """
        Método para guardar una colonia en la base de datos.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        db.session.add(self)
        db.session.commit()
        return 'Colonia guardada', 200
        
    def eliminar(self):
        """
        Método para eliminar una colonia de la base de datos.

        Retorno:
            str, int: Mensaje de éxito y código de estado HTTP.
        """
        db.session.delete(self)
        db.session.commit()
        return 'Colonia eliminada.', 201
        
    @classmethod
    def obtener_colonia_por_id(cls, id):
        """
        Método de clase para obtener una colonia por su ID.

        Argumentos:
            id (int): ID de la colonia a buscar.

        Retorno:
            Colonia: La colonia buscada o None si no se encuentra.
        """
        return cls.query.get(id)
    
    @classmethod
    def obtener_colonias(cls):
        """
        Método de clase para obtener todas las colonias.

        Retorno:
            list: Lista de todas las colonias.
        """
        return cls.query.all()
    
    @classmethod
    def obtener_colonia_por_nombre(cls, nombre):
        """
        Método de clase para obtener una colonia por su nombre.

        Argumentos:
            nombre (str): Nombre de la colonia a buscar.

        Retorno:
            Colonia: La colonia buscada o None si no se encuentra.
        """
        return cls.query.filter_by(nombre_colonia=nombre).first()
    
    @classmethod
    def obtener_colonias_de_delegacion(cls, id_delegacion):
        """
        Método de clase para obtener todas las colonias de una delegación.

        Argumentos:
            id_delegacion (int): ID de la delegación cuyas colonias se quieren buscar.

        Retorno:
            list: Lista de las colonias de la delegación buscada.
        """
        return cls.query.filter_by(cve_delegacion=id_delegacion).all()