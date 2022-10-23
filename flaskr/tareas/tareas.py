import os
import pathlib
from celery import Celery
from pydub import AudioSegment
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from ..modelos import Tarea, db
import requests
celery_app = Celery(__name__)
# db.init_app(__name__)


@celery_app.task()
def convert_file(task_id, filename, newFormat, base_url, correo):
    file_split = filename.split('.')
    original_format = file_split[-1]
    work_path = pathlib.Path().resolve()
    filepath = os.path.join(work_path, 'flaskr', 'uploads', filename)
    audio = AudioSegment.from_file(filepath, original_format)
    new_file_name = filename.replace(original_format, newFormat)
    new_audio = audio.export(os.path.join(
        work_path, 'flaskr', 'uploads', new_file_name), format=newFormat)
    requests.post(
        "https://api.mailgun.net/v3/sandbox232d977beba44270bb923ebd87bfffb8.mailgun.org/messages",
        auth=("api", "adaa500700e6d32a872721419cfb1b53-29561299-50b00366"),
        data={"from": "Excited User <mailgun@sandbox232d977beba44270bb923ebd87bfffb8.mailgun.org>",
                      "to": [correo],
                      "subject": "Conversión audio",
              "text": f"Su audio con identificador {task_id} ha terminado su proceso de conversión!"})
    # tarea = Tarea.query.get_or_404(task_id)
    # tarea.status = 'processed'
    # tarea.url_destino = base_url + new_file_name
    # db.session.commit()
