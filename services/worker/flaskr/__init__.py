from flask_restful import Api
from flask import Flask, send_from_directory, jsonify

from .modelos import db, Usuario
from .tareas import convert_file
from flask_jwt_extended import JWTManager, get_jwt_identity

app = Flask(__name__)
app.config.from_object("flaskr.config.Config")


app_context = app.app_context()
app_context.push()

db.init_app(app)


@app.route('/api/tasks/<int:id>')
def tasks(id):
    convert_file.delay(id)
    return {"mensaje": "ok"}, 200


@app.route("/")
def hello_world():
    return jsonify(hello="world")


api = Api(app)

jwt = JWTManager(app)
