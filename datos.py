# Ruta /mostrar_sitios
## Devuelve
[
    {
        "cve_sitio": int,
        "nombre_sitio": str,
        "costo_promedio": float,
        "cve_tipo_sitio": int,
        "imagenes": [
            {
                "cve_foto_sitio": int,
                "link_imagen": str,
            },
        ],
        "delegacion": str,
        "calificacion": float,
    }
]


[
    {
        "cve_etiqueta": 1,
        "nombre": "Ciencia y tecnología"
    }
]




# Ruta /mostrar_sitio/<int:cve_sitio>
## Entrada
    obligatorio: cve_sitio
    opcional: token
    
# Salida
{
    "cve_sitio": ,
    "nombre_sitio": ,
    "longitud": ,
    "latitud": ,
    "descripcion": ,
    "correo": ,
    "costo": ,
    "pagina_web": ,
    "telefono": ,
    "adscripcion": ,
    "num_calificaciones": ,
    "calificacion": ,
    "horarios": [
        {
            "cve_horario": ,
            "dia": ,
            "horario_apertura": ,
            "horario_cierre": ,
        }
    ],
    "fotos": [
        {
            "cve_etiqueta": ,
            "nombre_etiqueta": ,
        }
    ],
    "colonia": ,
    "delegacion": ,
    "tipo_sitio": ,
    "comentarios": [
        {
            "cve_comentario": ,
            "comentario": ,
            "fecha_comentario": ,
            "fotos_comentario": [
                {
                    "cve_foto_comentario": ,
                    "link_imagen
                }
            ]
        }
    ]
    "me_gusta"
}


## crear_comentario

## Entrada

- token
- comentario 
- calificacion
- fotografias []

## Salida
- mensaje

########################
modificar_comentario
########################
## Entrada

- token
- cve_comentario
- calificacion
- comentario

## Salida
- mensaje

########################
eliminar_cuenta
########################
## Entrada
-token
- contrasena

## Salida
-mensaje

#######################
agregar_favorito
#######################

## Entrada
- token
- cve_sitio

## Salida
- mensaje

######################
inhabilitar_sitio
######################

## Entrada
- token
- cve_sitio

## Salida
- mensaje

#####################
eliminar_sitio
#####################

## Entrada
- Token
- cve_sitio

## Salida
- mensaje

#####################
generar_reglas
#####################

## Entrada
- token

## Salida
- mensaje

#####################
mostrar_usuarios
#####################

## Entrada
- token

## Salida
- usuario
- num_calificaciones
- num_comentarios
- promedio_calificacion

######################
inhabilitar_usuario
######################

## Entrada
- token
- usuario

## Salida
- mensaje

######################
mostrar_recomendaciones
######################

## Entrada
- token

## Salida
- sitios


######################
mostrar_favoritos
######################
