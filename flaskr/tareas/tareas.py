import os
import pathlib
from celery import Celery
from pydub import AudioSegment
from werkzeug.utils import secure_filename
celery_app = Celery(__name__)
UPLOAD_FOLDER = 'uploads'


@celery_app.task()
def add_together(a, b):
    return a+b


@celery_app.task()
def convert_file(filename, filepath, newFormat):
    # filepath = os.path.join('flaskr', UPLOAD_FOLDER, filename)
    filename = 'test.mp3'
    AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.prober = "C:\\ffmpeg\\bin\\ffprobe.exe"
    file_split = filename.split('.')
    original_format = file_split[-1]
    work_path = pathlib.Path().resolve()
    filepath = os.path.join(work_path, 'flaskr', 'uploads', filename)
    import pdb
    pdb.set_trace()
    audio = AudioSegment.from_file(filepath, original_format)
    pdb.set_trace()
    new_audio = audio.export("mashup.wav", format="wav")
