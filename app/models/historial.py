from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from .usuario import Usuario
from .sitio import Sitio
from app.classes.validacion import Validacion

class Historial(db.Model):
    cve_historial = db.Column(db.Integer, primary_key=True)
    me_gusta = db.Column(db.Boolean, default=False)
    fecha_visita = db.Column(db.DateTime, nullable=False)
    cve_usuario = db.Column(db.String(100), db.ForeignKey('usuario.correo_usuario'), nullable=False)
    cve_sitio = db.Column(db.Integer, db.ForeignKey('sitio.cve_sitio'), nullable=False)
    
    usuario = db.relationship('Usuario', backref='historiales')
    sitio = db.relationship('Sitio', backref='historiales')

    def to_dict(self):
        """
        Convertir el objeto del Historial a un diccionario.

        Retorno:
            dict: Diccionario que representa el Historial.
        """
        return {
            'cve_historial': self.cve_historial,
            'me_gusta': self.me_gusta,
            'fecha_visita': self.fecha_visita,
            'cve_tipo_usuario': self.cve_tipo_usuario,
            'cve_usuario': self.cve_usuario,
            'cve_sitio': self.cve_sitio,
        }

    @staticmethod
    def agregar_historial(cve_usuario, cve_sitio):
        """
        Se agrega un historial a la base de datos.

        Entrada:
            cve_usuario (str): Clave del usuario que realiza la visita.
            cve_sitio (int): Clave del sitio visitado.
            
        Retorno exitoso:
            True: Se ha agregado el historial a la base de datos.
            
        Retorno fallido:
            False: Hubo un error al agregar el historial a la base de datos.
        """
        try:
            
            historial_encontrado = Historial.query.filter_by(cve_usuario=cve_usuario, cve_sitio=cve_sitio).first()
            print(historial_encontrado)
            if historial_encontrado:
                historial_encontrado.fecha_visita = datetime.now()
                db.session.commit()
                return True
            
            nuevo_historial = Historial(
                me_gusta = 0,
                fecha_visita = datetime.now(),
                cve_usuario = cve_usuario,
                cve_sitio = cve_sitio
            )
            
            db.session.add(nuevo_historial)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False
            
    @staticmethod
    def modificar_me_gusta(cve_historial):
        """
        Modifica el estado de "me_gusta" del historial.

        Entrada:
            cve_historial (int): Clave del historial.
            
        Retorno exitoso:
            True: Se hizo la modificación.
        
        Retorno fallido:
            False: Hubo un error.
        """
        try:
            historial_encontrado = Historial.obtener_historial(cve_historial)
            
            if Validacion.valor_nulo(historial_encontrado):
                return False
            
            if historial_encontrado.me_gusta:
                historial_encontrado.me_gusta = False
            else:
                historial_encontrado.me_gusta = True
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def eliminar_historial(cve_historial):
        """
        Se elimina el historial de la base de datos.
        
        Entrada:
            cve_historial (int): Clave de historial.
            
        Retorno:
            boolean: True si se eliminó o False si no.
        """
        try:
            historial_encontrado = Historial.obtener_historial(cve_historial)
            
            if historial_encontrado:
                db.session.delete(historial_encontrado)
                db.session.commit()
                return True
            return False
                
        except Exception as e:
            print("Hubo un error: ", e)
            return False

    @staticmethod
    def obtener_historial(cve_historial):
        """
        Obtener un historial por su clave.

        Entrada:
            cve_historial (int): Clave del historial.

        Retorno exitoso:
            Historial: Instancia de tipo Historial.
            
        Retorno fallido:
            None: No se encontró o hubo un error.
        """
        try:
            
            historial_encontrado = Historial.query.get(cve_historial)
            
            if not Validacion.valor_nulo(historial_encontrado):
                return historial_encontrado
            else:
                return None
        except Exception as e:
            print("Hubo un error: ", e)
            return None

    @staticmethod
    def obtener_historiales_por_sitio(cve_sitio):
        """
        Consulta todos los historiales asociados a un sitio.

        Entrada:
            cve_sitio (int): Clave del sitio.

        Retorno exitoso:
            list: Lista de instancias de tipo Historial.
            
        Retorno fallido:
            None: Hubo un error o no hay historial que mostrar.
        """
        try:
            
            historiales_encontrados = Historial.query.filter_by(cve_sitio=cve_sitio).all()
            if Validacion.valor_nulo(historiales_encontrados):
                return None

            return historiales_encontrados
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_historiales_por_usuario(cve_usuario):
        """
        Obtener todos los historiales asociados a un usuario.

        Entrada:
            cve_usuario (str): Clave del usuario.

        Retorno exitoso:
            list: Lista de instancias de tipo Historial.
            
        Retorno fallido:
            None: Hubo un error o no hay historial que mostrar.
        """
        try:
            
            historiales_encontrados = Historial.query.filter_by(cve_usuario=cve_usuario).all()
            if Validacion.valor_nulo(historiales_encontrados):
                return None

            return historiales_encontrados
        except Exception as e:
            print("Hubo un error: ", e)
            return None
    
    @staticmethod
    def obtener_historiales_recientes():
        """
        Obtener todos los historiales ordenados de manera descendente por fecha de visita.

        Retorno exitoso:
            list: Lista de instancias de tipo Historial.
            
        Retorno fallido:
            None: No se encontraron historiales.
        """
        try:
            historiales_encontrados = Historial.query.order_by(Historial.fecha_visita.desc()).all()
            
            if Validacion.valor_nulo(historiales_encontrados):
                return None
            return historiales_encontrados
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        
    @staticmethod
    def obtener_historiales_por_megusta(cve_usuario):
        """
        Consulta todos los historiales de un usuario que coinciden con una preferencia "me_gusta".

        Entrada:
            cve_usuario (str): Clave del usuario.

        Retorno exitoso:
            list: Lista de instancias de tipo Historial.
            
        Retorno fallido:
            None: No se encontraron o hubo errores.
        """
        try:
            
            historiales_encontrados = Historial.query.filter_by(cve_usuario=cve_usuario, me_gusta = True).all()
            
            if Validacion.valor_nulo(historiales_encontrados):
                return None
            
            return historiales_encontrados
            
        except Exception as e:
            print("Hubo un error: ", e)
            return None
        
    @staticmethod
    def contar_visitas_por_sitio_en_fecha(cve_sitio, fecha_inicio = None, fecha_fin = None):
        """
        Cuenta las visitas a un sitio en un rango de fechas.

        Entrada:
            cve_sitio (int): Clave del sitio.
            fecha_inicio (datetime): Fecha de inicio del rango.
            fecha_fin (datetime): Fecha de fin del rango.

        Retorno exitoso:
            dict: Diccionario con la cantidad de visitas.
        
        Retorno fallido:
            None: Hubo un error.
        """
        try:
            if Validacion.valor_nulo(fecha_inicio):
                fecha_inicio = datetime.now() - timedelta(days=7)
            if Validacion.valor_nulo(fecha_fin):
                fecha_fin = datetime.now()
                
            count = db.session.query(func.count(Historial.cve_historial)).filter(
                Historial.cve_sitio == cve_sitio,
                Historial.fecha_visita >= fecha_inicio,
                Historial.fecha_visita <= fecha_fin
            ).scalar()
            return {'visitas': count}
        except Exception as e:
            print("Hubo un error: ", e)
            return None



