from .consulta import Consulta

def modificar_sitio(cve_sitio, nombre_sitio, x_longitud, y_latitud, direccion, 
                    cve_tipo_sitio, cve_delegacion, colonia, 
                    descripcion, correo, costo_promedio, pagina_web, 
                    telefono, adscripcion, horarios: list, etiquetas: list, servicios: list
                    ):
    conexion_db = Consulta()
    
    try:
        conexion_db.cursor.callproc('modificar_sitio', [cve_sitio, nombre_sitio, x_longitud, y_latitud, direccion, cve_tipo_sitio, cve_delegacion, colonia, descripcion, correo, costo_promedio, pagina_web, telefono, adscripcion])
        
        if horarios:
            for horario in horarios:
                conexion_db.cursor.callproc('modificar_sitio_horario', [cve_sitio, horario["dia"], horario["horario_apertura"],    horario["horario_cierre"]])
        
        if etiquetas:    
            for cve_etiqueta in etiquetas:
                conexion_db.cursor.callproc('modificar_sitio_etiqueta', [cve_sitio, cve_etiqueta])
        
        if servicios:   
            for cve_servicio in servicios:
                conexion_db.cursor.callproc('modificar_sitio_servicio', [cve_sitio, cve_servicio])
    
    finally:
        conexion_db.cerrar_conexion_db
        