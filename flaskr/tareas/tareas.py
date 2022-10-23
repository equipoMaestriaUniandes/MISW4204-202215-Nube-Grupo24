import os
import pathlib
from celery import Celery
from pydub import AudioSegment
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from ..modelos import Tarea, db
celery_app = Celery(__name__)
# db.init_app(__name__)


@celery_app.task()
def convert_file(task_id, filename, newFormat, base_url):
    file_split = filename.split('.')
    original_format = file_split[-1]
    work_path = pathlib.Path().resolve()
    filepath = os.path.join(work_path, 'flaskr', 'uploads', filename)
    audio = AudioSegment.from_file(filepath, original_format)
    new_file_name = filename.replace(original_format, newFormat)
    new_audio = audio.export(os.path.join(
        work_path, 'flaskr', 'uploads', new_file_name), format=newFormat)
    # tarea = Tarea.query.get_or_404(task_id)
    # tarea.status = 'processed'
    # tarea.url_destino = base_url + new_file_name
    # db.session.commit()
