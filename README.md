## 1. Clonar el repositorio

git clone https://github.com/krujodrkf/django.git

## 2.  Construir el proyecto

cd django/countries_project/

docker compose build


## 3.  Desplegar el proyecto

docker compose up

## 3. Acceder al endpoint REST:

Ver listado de todos los países: http://localhost:8100/api/countries

Ver un país en particular: http://localhost:8100/api/countries/{id}
 