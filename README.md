## 1. Clonar el repositorio

Primero, clona el repositorio desde GitHub:

git clone https://github.com/krujodrkf/django.git

cd django

## 2.  Construir y levantar el entorno utilizando Docker
docker-compose build

docker-compose up


Utilizará los puertos:

Django en el puerto 8100

PostgreSQL en el puerto 5434

Redis en el puerto 6379

## 3. Ejecutar:
docker-compose run celery_worker

docker-compose run celery_beat

## 4. Acceder al endpoint REST:
http://localhost:8100   