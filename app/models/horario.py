from app import db
from app.classes.validacion import Validacion

class Horario(db.Model):
    cve_horario = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(100), nullable=False)
    horario_apertura = db.Column(db.Time, nullable=False)
    horario_cierre = db.Column(db.Time, nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio') , nullable=False)
    
    sitio = db.relationship('Sitio', backref='horarios')

    def to_dict(self):
        """
        Convertir el objeto del horario a un diccionario.

        Retorno:
            dict: Diccionario que representa el sitio.
        """
        return {
            'cve_horario': self.cve_horario,
            'dia': self.dia,
            'horario_apertura': str(self.horario_apertura),
            'horario_cierre': str(self.horario_cierre),
            'cve_sitio': self.cve_sitio
        }

    @staticmethod
    def agregar_horario(dia, horario_apertura, horario_cierre, cve_sitio):
        """
        Agregar un nuevo horario a la base de datos.

        Entrada:
            dia (str): Día de la semana.
            horario_apertura (Time): Hora de apertura del sitio.
            horario_cierre (Time): Hora de cierre del sitio.
            cve_sitio (int): Clave del sitio al que pertenece este horario.
        
        Retorno exitoso:
            True: Se ha agregado el horario a la base de datos.
        
        Retorno fallido:
            False: Ha ocurrido un error.
        """
        try:
            horario_nuevo = Horario(
                dia = dia,
                horario_apertura = horario_apertura,
                horario_cierre = horario_cierre,
                cve_sitio = cve_sitio 
            )
            db.session.add(horario_nuevo)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
        
    @staticmethod
    def actualizar_horario(cve_horario, dia, horario_apertura, horario_cierre):
        """
        Actualizar los datos de un horario.

        Entrada obligatoria:
            cve_horario (int): Clave del horario a actualizar.
            
        Entrada opcional:
            dia (str): Nuevo día de la semana.
            horario_apertura (time): Nueva hora de apertura del sitio.
            horario_cierre (time): Nueva hora de cierre del sitio.
        
        Retorno exitoso:
            True: Se han hecho las actualizaciones.
            
        Retorno fallido:
            False: Hubo un problema.
        """
        try:
            horario_encontrado = Horario.obtener_horario_por_cve(cve_horario)
            
            if not Validacion.valor_nulo(dia):
                horario_encontrado.dia = dia
            if not Validacion.valor_nulo(horario_apertura):
                horario_encontrado.horario_apertura = horario_apertura
            if not Validacion.valor_nulo(horario_cierre):
                horario_encontrado.horario_cierre = horario_cierre
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
        
    @staticmethod
    def eliminar_horario(cve_horario):
        """
        Elimina un horario en específico.

        Entrada:
            cve_horario (int): Clave del horario a eliminar.

        Retorno exitoso:
            True: Se ha eliminado correctamente de la base de datos.
            
        Retorno fallido:
            False: Hubo un error al querer eliminarlo.
        """
        try:
            horario_encontrado = Horario.obtener_horario_por_cve(cve_horario)
            if not Validacion.valor_nulo(horario_encontrado):
                db.session.delete(horario_encontrado)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Hubo un problema: ", e)
            return False

    @staticmethod
    def obtener_horario_por_cve(cve_horario):
        """
        Obtener un horario específico por su clave.

        Entrada:
            cve_horario (int): Clave del horario a consultar.

        Retorno exitoso:
            Horario: Instancia de Horario.
            
        Retorno fallido:
            None: No se encontró el horario u ocurrió un error.
        """
        try:
            horario_encontrado = Horario.query.get(cve_horario)

            if not Validacion.valor_nulo(horario_encontrado):
                return horario_encontrado
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_horarios_por_sitio(cve_sitio):
        """
        Obtener todos los horarios de un sitio en específico.

        Entrada:
            cve_sitio (int): Clave del sitio a consultar.

        Retorno exitoso:
            list: Lista de instancias de tipo Horario.
        
        Retorno fallido:
            None: No se encontraron horario o hubo un error.
        """
        try:
            horarios_encontrados = Horario.query.filter_by(cve_sitio=cve_sitio).all()
            if not Validacion.valor_nulo(horarios_encontrados):
                return horarios_encontrados
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    