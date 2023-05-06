# TT_Backend

## Crear entorno virtual

virtualenv venv

## Instalar todos los paquetes

pip install -r requirements.txt

## Configurar archivo .env (no incluido en el proyecto)

Tanto SECRET_KEY_DB y SECRET_KEY_TOKEN se generaron aleatoriamente. Se puede cambiar por otra.

1. DATABASE_URL=mysql+pymysql://usuario_en_mysql:contraseña_de_usuario@localhost/nombre_de_base_de_datos
2. SECRET_KEY_DB=a795a7e48d191f8b8a0487fb233a98f0
3. SECRET_KEY_TOKEN=a7957e48f8b7e48d187fb98f3a98f0

## Hacer las migraciones

1. Inicializar migraciones: flask db init
2. Crear una migración: flask db migrate -m "mensaje de la migración"
3. Aplica la migración: flask db upgrade