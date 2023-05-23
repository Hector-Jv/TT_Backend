from app import db

class Colonia(db.Model):
    cve_colonia = db.Column(db.Integer, primary_key=True)
    nombre_colonia = db.Column(db.String(400), nullable=False)
    cve_delegacion = db.Column(db.Integer, db.ForeignKey('delegacion.cve_delegacion') , nullable=False)
    
    delegacion = db.relationship('Delegacion', backref='colonias')
    
    def to_dict(self):
        """
        Convertir el objeto de la colonia a un diccionario.

        Retorno:
            dict: Diccionario que representa la colonia.
        """
        return {
            'cve_colonia': self.cve_colonia,
            'nombre_colonia': self.nombre_colonia,
            'cve_delegacion': self.cve_delegacion
        }

    @staticmethod
    def agregar_colonia(nombre_colonia, cve_delegacion):
        """
        Agregar una nueva colonia a la base de datos.

        Entrada:
            nombre_colonia (str): Nombre que va a tener la colonia.
            cve_delegacion (int): Clave de la delegación a la que pertenece la colonia.
            
        Retorno exitoso:
            True: Se a guardado correctamente la colonia.
        
        Retorno fallido:
            False: Hubo algún problema y no se pudo guardar la colonia.
        """
        if Colonia.obtener_colonia_por_nombre(nombre_colonia):
            return False
        
        try:
            colonia = Colonia(
                nombre_colonia = nombre_colonia,
                cve_delegacion = cve_delegacion
            )
            db.session.add(colonia)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error en función agregar_colonia: ", e)
            return False
    
    @staticmethod
    def eliminar_colonia(cve_colonia):
        """
        Eliminar una colonia de la base de datos.

        Entrada:
            cve_colonia (int): Clave que hace referencia a la colonia que se desea eliminar.
            
        Retorno exitoso:
            True: Se a eliminado correctamente la colonia.
        
        Retorno fallido:
            False: No se pudo eliminar la colonia.
        """
        try:
            colonia = Colonia.obtener_colonia_por_id(cve_colonia)
            if colonia:
                db.session.delete(colonia)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un error en función eliminar_colonia: ", e)
            return False
        
    @staticmethod
    def obtener_colonia_por_cve(cve_colonia):
        """
        Obtener una colonia por su clave.

        Entrada:
            clave (int): Clave de la colonia a buscar.

        Retorno exitoso:
            dict: Diccionario con los datos de la colonia buscada.
        
        Retorno fallido:
            None: No se encontró ninguna colonia con esa clave.
        """
        try:
            colonia = Colonia.query.get(cve_colonia)
            if colonia:
                return colonia
            else:
                return None
        except Exception as e:
            print("Hubo un error en función obtener_colonia_por_cve: ", e)
            return None
    
    @staticmethod
    def obtener_colonia_por_nombre(nombre):
        """
        Obtener una colonia por su nombre.

        Entrada:
            nombre (str): Nombre de la colonia a buscar.

        Retorno exitoso:
            Colonia: Instancia de tipo Colonia
            
        Retorno fallido:
            None: No se encontró los datos de la colonia ingresada.
        """
        try:
            colonia = Colonia.query.filter_by(nombre_colonia=nombre).first()
            if colonia is not None:
                return colonia
            else:
                None
        except Exception as e:
            print("Hubo un error en función obtener_colonia_por_nombre: ", e)
            return None
    
    @staticmethod
    def obtener_colonias_de_delegacion(id_delegacion):
        """
        Obtener todas las colonias de una delegación.

        Entrada:
            id_delegacion (int): ID de la delegación cuyas colonias se quieren buscar.

        Retorno exitoso:
            list: Lista de las colonias de la delegación buscada.
            
        Retorno fallido:
            None: Si no hay colonias con el cve_delegacion ingresado.
            
        """
        try:
            colonias = Colonia.query.filter_by(cve_delegacion=id_delegacion).all()
            if colonias:
                return colonias
            else:
                return None
        except Exception as e:
            print("Hubo un error en función obtener_colonias_de_delegacion", e)
            return None