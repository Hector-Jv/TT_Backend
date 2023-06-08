# TT_Backend

## Crear entorno virtual

virtualenv venv

## Instalar todos los paquetes

pip install -r requirements.txt

## Hacer las migraciones

1. Inicializar migraciones: flask db init
2. Crear una migración: flask db migrate -m "mensaje de la migración"
3. Aplica la migración: flask db upgrade