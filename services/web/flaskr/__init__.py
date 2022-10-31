from flask_restful import Api
from flask import Flask, send_from_directory, jsonify

from .modelos import db, Usuario
from .vistas import VistaTareas, VistaTarea, VistaLogIn, VistaSignIn
from flask_jwt_extended import JWTManager, get_jwt_identity

app = Flask(__name__)
app.config.from_object("flaskr.config.Config")


app_context = app.app_context()
app_context.push()

db.init_app(app)


@app.route('/api/files/<path:filename>')
def serve_page(filename):
    identity = get_jwt_identity()
    user = Usuario.query.filter_by(correo=identity).first()
    return send_from_directory(app.config["MEDIA_FOLDER"] + f"/{user.id}", filename)


@app.route("/")
def hello_world():
    return jsonify(hello="world")


api = Api(app)
api.add_resource(VistaTareas, '/api/tasks')
api.add_resource(VistaTarea, '/api/tasks/<int:id_task>')
api.add_resource(VistaLogIn, '/api/login')
api.add_resource(VistaSignIn, '/api/signin')

jwt = JWTManager(app)
