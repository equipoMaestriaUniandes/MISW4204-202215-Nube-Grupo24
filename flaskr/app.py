from flaskr import create_app
from flask_restful import Api
from flask import Flask, send_from_directory

from .modelos import db
from .vistas import *
from flask_jwt_extended import JWTManager

UPLOAD_FOLDER = 'C:/uploads'
app = Flask(__name__, static_folder=os.path.join(
    os.path.dirname(__file__), 'build'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory('uploads', path)


app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaTareas, '/tareas')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaSignIn, '/signin')


jwt = JWTManager(app)
