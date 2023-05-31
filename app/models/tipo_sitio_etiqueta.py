from app import db

class TipoSitio_Etiqueta(db.Model):
    cve_tipo_sitio = db.Column(db.Integer, primary_key=True)
    cve_etiqueta = db.Column(db.Integer, primary_key=True)
    
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['cve_tipo_sitio'],
            ['tipo_sitio.cve_tipo_sitio'],
        ),
        db.ForeignKeyConstraint(
            ['cve_etiqueta'],
            ['etiqueta.cve_etiqueta'],
        ),
    )
    
    @staticmethod
    def agregar_relacion(cve_tipo_sitio, cve_etiqueta):
        """
        Agregar una nueva relación entre tipo sitio y etiqueta.

        Entrada:
            cve_tipo_sitio (int): Clave del tipo sitio.
            cve_etiqueta (int): Clave de la etiqueta.

        Retorno exitoso:
            True: Se ha agregado una nueva relación a la base de datos.
            
        Retorno fallido:
            False: Existe ya una relación o hubo un error.
        """
        try:
            relacion = TipoSitio_Etiqueta.query.filter_by(cve_tipo_sitio=cve_tipo_sitio, cve_etiqueta=cve_etiqueta).first()
            
            if relacion:
                return False
            
            nueva_relacion = TipoSitio_Etiqueta(
                cve_tipo_sitio=cve_tipo_sitio, 
                cve_etiqueta=cve_etiqueta
            )
            db.session.add(nueva_relacion)
            db.session.commit()
            return True
        except Exception as e:
            print("Hubo un error: ", e)
            return False