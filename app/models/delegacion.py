from app import db

class Delegacion(db.Model):
    cve_delegacion = db.Column(db.Integer, primary_key=True)
    nombre_delegacion = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre_delegacion):
        """
        Método constructor de la clase Delegacion.

        Argumentos:
            nombre_delegacion (str): Nombre de la delegación.
        """
        self.nombre_delegacion = nombre_delegacion
        db.session.add(self)
        db.session.commit()
        
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
    def mostrar_todos():
        """
        Método estático para mostrar todas las delegaciones.

        Retorno:
            list: Lista de todas las delegaciones o mensaje de error si no existen.
        """
        delegaciones = Delegacion.query.all()
        if delegaciones:
            return [delegacion.to_dict() for delegacion in delegaciones], 200
        else:
            return 'No se encontraron delegaciones', 404

    @staticmethod
    def buscar_por_cve(cve):
        """
        Método estático para buscar una delegación por su clave.

        Argumentos:
            cve (int): Clave de la delegación a buscar.

        Retorno:
            Delegacion or tuple: La delegación buscada o mensaje de error y código de estado HTTP si no se encuentra.
        """
        delegacion = Delegacion.query.filter_by(cve_delegacion=cve).first()
        if delegacion:
            return delegacion.to_dict(), 200
        else:
            return 'Delegación no encontrada', 404
