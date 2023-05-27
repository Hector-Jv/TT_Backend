import mysql.connector
from datetime import datetime, date

class Consulta():
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='root',
            password='hBEIGoZroJvoO8aVhn1h',
            host='containers-us-west-45.railway.app',
            database='railway',
            port='5922'
        )
        self.cursor = self.conn.cursor()
    
    def cerrar_conexion_db(self):
        self.cursor.close()
        self.conn.close()
    
    def obtener_sitios(self, cve_tipo_sitio: int = 1, orden: int = 1, pagina: int = 0):
        """
        , precio_min: float = 0, precio_max: float = 9999, calificacion_min: int = 0, cve_delegacion: int = 0
        , precio_min, precio_max, calificacion_min, cve_delegacion
        Obtiene todos los sitios con los datos necesarios para la ruta mostrar_sitios.
        
        Entrada:
            cve_tipo_sitio (int): Clave del tipo sitio
            orden (int): Opción de orden de datos.
            pagina (int): Paginación.
            precio_min (float): Filtro precio mínimo.
            precio_max (float): Filtro precio máximo.
            calificación_min (int): Filtro calificación mínima.
            cve_delegación (int): Filtro delegación
            
        Retorna:
            list: Lista de diccionarios con los datos de los sitios.
            int: Número de sitios encontrados.
            
        """
        sitios = []
        pagina *= 10
        num_sitios = 0
        try:
            self.cursor.callproc('obtener_sitios', [cve_tipo_sitio, orden, pagina])
            resultados = self.cursor.stored_results()
            
            for resultado in resultados:
                for sitio in resultado.fetchall():
                    num_sitios += 1
                    datos = {}
                    datos["cve_sitio"] = sitio[0]
                    datos["nombre_sitio"] = sitio[1]
                    datos["x_longitud"] = sitio[2]
                    datos["y_latitud"] = sitio[3]
                    datos["pagina_web"] = sitio[4]
                    datos["tipo_sitio"] = sitio[5]
                    datos["nombre_delegacion"] = sitio[6]
                    datos["nombre_colonia"] = sitio[7]
                    datos["visitas"] = sitio[8]
                    datos["calificacion"] = sitio[9]
                    datos["lista_fotos"] = self.obtener_info_fotos_sitio(datos["cve_sitio"])
                    
                    sitios.append(datos)
        finally:
            return sitios, num_sitios

    def obtener_info_fotos_sitio(self, cve_sitio: int):
        fotos = []
        try:
            self.cursor.callproc('obtener_imagenes_sitio', [cve_sitio])
            resultados = self.cursor.stored_results()
            for resultado in resultados:
                for foto in resultado.fetchall():
                    datos = {}
                    datos["nombre_imagen"] = foto[0]
                    datos["link_imagen"] = foto[1]
                    datos["nombre_autor"] = foto[2]
                    
                    fotos.append(datos)
        finally:
            return fotos
    
    def obtener_sitio(self, cve_sitio):
        datos = {}
        imagenes = []
        horarios = []
        comentarios = []
        try:
            self.cursor.callproc('obtener_sitio', [cve_sitio])
            resultados = self.cursor.stored_results()
            
            for resultado in resultados:
                datos_resultado = resultado.fetchall()
                if resultado.description[0][0] == 'cve_sitio':
                    sitio = datos_resultado[0]
                    datos["cve_sitio"] = sitio[0]
                    datos["nombre_sitio"] = sitio[1]
                    datos["x_longitud"] = sitio[2]
                    datos["y_latitud"] = sitio[3]
                    datos["direccion"] = sitio[4]
                    datos["fecha_actualizacion"] = str(sitio[5])
                    datos["descripcion"] = sitio[6]
                    datos["correo_sitio"] = sitio[7]
                    datos["fecha_fundacion"] = str(sitio[8])
                    datos["costo_promedio"] = sitio[9]
                    datos["habilitado"] = sitio[10]
                    datos["pagina_web"] = sitio[11]
                    datos["telefono"] = sitio[12]
                    datos["adscripcion"] = sitio[13]
                elif resultado.description[0][0] == 'nombre_servicio':
                    datos["servicios"] = [x[0] for x in datos_resultado] 
                elif resultado.description[0][0] == 'nombre_etiqueta':
                    datos["etiquetas"] = [x[0] for x in datos_resultado]
                elif resultado.description[0][0] == 'nombre_imagen':
                    imagen = datos_resultado[0]
                    dato_imagen = {}
                    dato_imagen["nombre_imagen"] = imagen[0]
                    dato_imagen["link_imagen"] = imagen[1]
                    dato_imagen["nombre_autor"] = imagen[2]
                    imagenes.append(dato_imagen)
                elif resultado.description[0][0] == 'dia':
                    horario = datos_resultado[0]
                    dato_horario = {}
                    dato_horario["dia"] = horario[0]
                    dato_horario["horario_apertura"] = str(horario[1])
                    dato_horario["horario_cierre"] = str(horario[2])
                    horarios.append(dato_horario)
                elif resultado.description[0][0] == 'visitas':
                    visita_datos = datos_resultado[0]
                    datos["visita"] = visita_datos[0]
                    datos["calificacion_promedio"] = visita_datos[1]
                elif resultado.description[0][0] == 'cve_comentario':
                    comentario = datos_resultado[0]
                    dato_comentario = {}
                    imagenes_comentario = []
                    dato_comentario["cve_comentario"] = comentario[0]
                    dato_comentario["comentario"] = comentario[1]
                    dato_comentario["fecha_comentario"] = str(comentario[2])
                    self.cursor.callproc('obtener_imagenes_fotocomentario', [comentario[0]])
                    imagenes_consulta = self.cursor.stored_results()
                    for imagenes in imagenes_consulta:
                        imagenes_resultado = imagenes.fetchall()
                        if imagenes.description[0][0] == 'nombre_imagen':
                            dato_imagen_comentario = {}
                            dato_imagen_comentario["nombre_imagen"] = imagenes_resultado[0]
                            dato_imagen_comentario["link_imagen"] = imagenes_resultado[1]
                            dato_imagen_comentario["nombre_autor"] = imagenes_resultado[2]
                            imagenes_comentario.append(dato_imagen_comentario)
                    dato_comentario["imagenes"] = imagenes_comentario
                    comentarios.append(dato_comentario)
                    
        finally:
            datos["imagenes"] = imagenes
            datos["horarios"] = horarios
            datos["comentarios"] = comentarios
            return datos
