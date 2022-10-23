from flaskr import create_app
from flask_restful import Api
from flask import Flask, send_from_directory

from .modelos import db
from .vistas import *
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER = 'C:/uploads'
app = create_app('default')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/api/files/<path:path>')
def serve_page(path):
    return send_from_directory('uploads', path)


app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaTareas, '/api/tasks')
api.add_resource(VistaTarea, '/api/tasks/<int:id_task>')
api.add_resource(VistaLogIn, '/api/login')
api.add_resource(VistaSignIn, '/api/signin')


jwt = JWTManager(app)
