import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'secret_key'
    PROPAGATE_EXCEPTIONS = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/flaskr/media"
    GOOGLE_STORAGE_LOCAL_DEST = f"{os.getenv('APP_FOLDER')}/flaskr/media"
    GOOGLE_STORAGE_SIGNATURE = {"expiration": timedelta(minutes=5)},
    GOOGLE_STORAGE_FILES_BUCKET = "converter_uniandes_24"
