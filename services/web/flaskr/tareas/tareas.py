import json
from dotenv import load_dotenv
import os
import pathlib
from celery import Celery
from pydub import AudioSegment
from flask_sqlalchemy import SQLAlchemy
from ..modelos import Tarea, db, Usuario
import requests

celery_app = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))


@celery_app.task()
def convert_file(task_id):
    tarea = Tarea.query.get_or_404(task_id)
    usuario = Usuario.query.get_or_404(tarea.usuario_id)
    filename = tarea.url_origen.split('/')[-1]
    file_split = filename.split('.')
    original_format = file_split[-1]
    filepath = os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media", filename)
    audio = AudioSegment.from_file(filepath, original_format)
    new_file_name = filename.replace(original_format, tarea.formato_nuevo)
    audio.export(os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media", new_file_name), format=tarea.formato_nuevo)
    mailgun_key = os.getenv('MAIL_KEY')
    mailgun_domain = os.getenv('MAIL_DOMAIN')
    # print('mailgun_key',mailgun_key)
    # print('mailgun_domain',mailgun_domain)
    print(usuario.correo)
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
