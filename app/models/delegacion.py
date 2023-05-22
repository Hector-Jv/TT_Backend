from app import db

class Delegacion(db.Model):
    cve_delegacion = db.Column(db.Integer, primary_key=True)
    nombre_delegacion = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """
        Convierte el objeto Delegacion a un diccionario.

        Retorno:
            dict: Representación en diccionario del objeto Delegacion.
        """
        return {
            'cve_delegacion': self.cve_delegacion,
            'nombre_delegacion': self.nombre_delegacion
        }
        
    @staticmethod
    def agregar_delegacion(nombre_delegacion):
        """
        Se agrega una delegacion a la base de datos.
        
        Retorno exitoso:
            True: Se ha guardado correctamente.
        
        Retorno fallido:
            False: Error al agregar la delegación.
        """
        try:
            nueva_delegacion = Delegacion(nombre_delegacion=nombre_delegacion)
            db.session.add(nueva_delegacion)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error al agregar la delegación.")
            return False
        
    @staticmethod
    def mostrar_todos_las_delegaciones():
        """
        Muestra todas las delegaciones guardadas en la base de datos.

        Retorno exitoso:
            list: Lista de todas las delegaciones.
        
        Retorno fallido:
            None: No se encontraron delegaciones guardadas.
        """
        try:
            delegaciones = Delegacion.query.all()
            if delegaciones:
                return delegaciones
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_delegacion_por_cve(cve):
        """
        Obtener delegación por su clave.

        Entrada:
            cve (int): Clave de la delegación a buscar.

        Retorno exitoso:
            Delegacion: Datos de la delegación buscada.
            
        Retorno fallido:
            None: No se encontró la delegación.
        """
        try:
            delegacion = Delegacion.query.filter_by(cve_delegacion=cve).first()
            if delegacion:
                return delegacion
            else:
                return None
        except Exception as e:
            print("Error al buscar la delegación.")
            return None
