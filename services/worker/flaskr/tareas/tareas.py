import json
from dotenv import load_dotenv
import os
from shutil import rmtree
from celery import Celery
from pydub import AudioSegment
from flask_sqlalchemy import SQLAlchemy
from ..modelos import Tarea, db, Usuario
import requests

from mimetypes import guess_type
from google.cloud import storage

celery_app = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))


@celery_app.task()
def convert_file(task_id):
    # Traer el registro de la tarea
    tarea = Tarea.query.get_or_404(task_id)
    # Traer el resgistro del usuario dasociado a la tarea
    usuario = Usuario.query.get_or_404(tarea.usuario_id)
    print(f"Comienza tarea {tarea.id}")
    # Set variables locales
    filename = tarea.url_origen.split('/')[-1]
    file_split = filename.split('.')
    original_format = file_split[-1]
    absolute_path = os.path.dirname(__file__)
    folderpath = os.path.join(absolute_path, f"flaskr/media/{usuario.correo}/{tarea.id}")
    os.makedirs(folderpath, exist_ok=True)
    filepath = os.path.join(folderpath, filename)
    new_file_name = filename.replace(original_format, tarea.formato_nuevo)
    filepath_new = os.path.join(folderpath, new_file_name)
    # Descargar archivo
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.getenv('BUCKET'))
    blob = bucket.blob(f"{usuario.correo}/{filename}")
    blob.download_to_filename(filepath)
    print("Converter audio")
    # Convertir Audio
    audio = AudioSegment.from_file(filepath, original_format)
    audio.export(filepath_new, format=tarea.formato_nuevo)
    print("Finaliza conversion audio")
    # Subir Archivo
    contentType = guess_type(new_file_name)[0]
    blob = bucket.blob(f"{usuario.correo}/{new_file_name}")
    blob.upload_from_filename(filepath_new, content_type=contentType)
    # Remover carpeta local
    rmtree(folderpath)
    # Envio de email
    mailgun_key = os.getenv('MAIL_KEY')
    mailgun_domain = os.getenv('MAIL_DOMAIN')
    respuesta_email = requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", mailgun_key),
        data={"from": f"Cloud member <mailgun@{mailgun_domain}>",
                      "to": [usuario.correo],
                      "subject": "Conversión audio",
              "text": f"Su audio con identificador {task_id} ha terminado su proceso de conversión!"})
    print(json.dumps(respuesta_email.text))
    tarea.status = 'processed'
    tarea.url_destino = tarea.url_origen.replace(original_format, tarea.formato_nuevo)
    db.session.commit()
