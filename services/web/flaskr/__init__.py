from flask_restful import Api
from flask import Flask, send_from_directory, jsonify, Response
import os

from .modelos import db, Usuario
from .vistas import VistaTareas, VistaTarea, VistaLogIn, VistaSignIn
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity

from google.cloud import storage


app = Flask(__name__)
app.config.from_object("flaskr.config.Config")


app_context = app.app_context()
app_context.push()

db.init_app(app)


@app.route('/api/files/<path:filename>')
@jwt_required()
def serve_page(filename):
    identity = get_jwt_identity()
    filename = f"{identity}/{filename}"
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.getenv('BUCKET'))
    blob = bucket.blob(filename)
    metadata = bucket.get_blob(filename)
    content = blob.download_as_string()
    return Response(content, mimetype=metadata.content_type)


@app.route("/")
def hello_world():
    return jsonify(hello="world")


api = Api(app)
api.add_resource(VistaTareas, '/api/tasks')
api.add_resource(VistaTarea, '/api/tasks/<int:id_task>')
api.add_resource(VistaLogIn, '/api/login')
api.add_resource(VistaSignIn, '/api/signin')

jwt = JWTManager(app)
