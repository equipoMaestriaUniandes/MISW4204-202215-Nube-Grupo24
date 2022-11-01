# MISW4204-202215-Nube-Grupo24
## Pasos para ejecutar de forma local

### Clonar el proyecto
En su computador abra una terminal donde desee clonar el proyecto y clonelo usando el comando

```git clone https://github.com/equipoMaestriaUniandes/MISW4204-202215-Nube-Grupo24.git```


### Crear los archivos .env
Dado la naturaleza del proyecto es necesario usar llaves privadas que se almacenan en un archivo ```.env.dev .env.prod .env.prod.amb .env.prod.db```. Estos archivos se deben crear dentro de la carpeta raiz del proyecto. Para obtener una copia de este archivo contacte a alguien del equipo de desarrolladores del proyecto.

Si desea crear su propio archivos tenga en cuenta que debe tener la siguiente estructura  
#### .env.dev
```
FLASK_APP=flaskr/__init__.py
FLASK_DEBUG=1
DATABASE_URL=postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
MAIL_KEY=
MAIL_DOMAIN=
CELERY_BROKER_URL=amqp://myuser:mypassword@rabbitmq/
APP_FOLDER=/usr/src/app
```
#### .env.prod
```
FLASK_APP=flaskr/__init__.py
FLASK_DEBUG=0
DATABASE_URL=postgresql://converter:converter@db:5432/converter_db
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
MAIL_KEY=
MAIL_DOMAIN=
CELERY_BROKER_URL=amqp://myuserprod:mypasswordprod@rabbitmq/
APP_FOLDER=/home/app/web
```
#### .env.prod.db
```
POSTGRES_USER=converter
POSTGRES_PASSWORD=converter
POSTGRES_DB=converter_db
```
#### .env.prod.amb
```
RABBITMQ_DEFAULT_USER=myuserprod
RABBITMQ_DEFAULT_PASS=mypasswordprod
```
En donde estas variables ```MAIL_KEY``` corresponde al api key y ```MAIL_DOMAIN``` corresponde al dominio de una cuenta de Mailgun. El proyecto se encuentra configurado para realizar el envío de correos con Mailgun por lo que si ingresa credenciales de otro servicio o desea usar otro servicio se debe modificar los archivos base del proyecto. 

### Docker
Para correr el proyecto debe tener instalado docker y docker-compose

### Ejecutar prod
1. Abra una consola y ubíquese sobre la raíz del proyecto. 

2. Corra el comando 

```docker-compose -f docker-compose.prod.yml up --build```

3. Abra otra consola y ubiquese sobre la raiz del proyecto y corra el comando

```docker-compose exec web celery -A flaskr.tareas.tareas worker -l info --pool=solo```
### Nube
en la carpeta despliegues se ecuentra las carpetas necesarias para correr las imagenes de docker en las maquinas virtuales
