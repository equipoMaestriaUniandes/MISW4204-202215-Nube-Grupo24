# MISW4204-202215-Nube-Grupo24
## Pasos para ejecutar de forma local

### Clonar el proyecto
En su computador abra una terminal donde desee clonar el proyecto y clonelo usando el comando

```git clone https://github.com/equipoMaestriaUniandes/MISW4204-202215-Nube-Grupo24.git```


### Crear el ambiente virtual
Para ejecutar el proyecto se debe crear un ambiente virtual en python siguiendo los siguientes pasos 

1. Ubiquese en la carpeta raíz del proyecto

2. Ejecute el siguiente comando (reemplace python por python3 si su sistema operativo lo requiere)

``` python -m venv venv ```

3. Active el ambiente virtual, si no sabe como en este [link](https://www.infoworld.com/article/3239675/virtualenv-and-venv-python-virtual-environments-explained.html) puede revisar los comandos dependiendo del sistema operativo en la sección "Activate the virtual environment"

4. Una vez tenga el ambiente activado instale todas las dependencias necesarias con el comando 

``` pip install -r requirements.txt ```

### Instalar ffmpeg a nivel de sistema operativo
Descargue e instale ffmpeg a nivel de sistema operativo, puede hacer esto accediendo a los link de descarga aprovisionados [aquí](https://ffmpeg.org/download.html)

Se recomienda buscar en internet como instalar correctamente ffmpeg en su sistema operativo si nunca lo ha instalado previamente o no recuerda como hacer su correcta instalación

### Crear el archivo .env
Dado la naturaleza del proyecto es necesario usar llaves privadas que se almacenan en un archivo .env. Este archivo se debe crear dentro de la carpeta "tareas". Para obtener una copia de este archivo contacte a alguien del equipo de desarrolladores del proyecto.

Si desea crear su propio .env tenga en cuenta que debe tener la siguiente estructura
```
MAIL_KEY=...
MAIL_DOMAIN=...
```
En donde estas variables corresponden al api key y dominio de una cuenta de Mailgun. El proyecto se encuentra configurado para realizar el envío de correos con Mailgun por lo que si ingresa credenciales de otro servicio o desea usar otro servicio se debe modificar los archivos base del proyecto. 


### Ejecutar flask
1. Abra una consola y ubíquese sobre la raíz del proyecto. 

2. Active el ambiente virtual tal cual lo hizo en [Crear el ambiente virtual](crear-el-ambiente-virtual)

3. Entre al directorio flaskr usando el comando 

```cd flaskr```

4. Ejecute el comando

```flask run```

### Ejecutar celery
Nota: Para correr celery es necesario instalar rabbitMQ a nivel de sistema operativo o tener un docker corriendo una imagen que corresponda a este broker

1. Abra una consola y ubíquese sobre la raíz del proyecto. 

2. Active el ambiente virtual tal cual lo hizo en [Crear el ambiente virtual](crear-el-ambiente-virtual)

3. Ejecute el comando

```celery -A flaskr.tareas.tareas worker -l info --pool=solo```
