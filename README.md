## 1. Clonar el repositorio

git clone https://github.com/krujodrkf/django.git

## 2.  Construir el proyecto

cd django/countries_project/

docker compose build


## 3.  Desplegar el proyecto

docker compose up

## 4. Conectarse a la shell de Python para llenar la tabla por 1ra vez

Ejecutar docker ps y copiar el Container ID de la imagen llamada django_django

docker exec -t -i {containerId} bash

python manage.py shell


En la shell de Python:

from countries_project.tasks import update_country_data

update_country_data()


## 5. Acceder al endpoint REST:

Ver listado de todos los países: http://localhost:8100/api/countries

Ver un país en particular: http://localhost:8100/api/countries/{id}
 