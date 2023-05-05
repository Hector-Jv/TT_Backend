import json

def data_lista_museos():
    with open('app/data/museo_directorio.json', 'r', encoding='utf-8') as file:
        datos_museo = json.load(file)

    listado = []
    dato = {}
        
    for elemento in datos_museo:
        
        dato["nombre_sitio"] = elemento["museo_nombre"]
        dato["x_longitud"] = elemento["gmaps_longitud"]
        dato[]
        listado.add((
            , 
            ,
            elemento["gmaps_latitud"],
            elemento["email"],
            elemento["pagina_web"],
            elemento["fecha_mod"],
            elemento["museo_cp"],
            elemento["museo_telefono1"],
            elemento["museo_calle_numero"],
            
            elemento["museo_tematica_n1"],
            elemento["museo_colonia"]
        ))

    return listado