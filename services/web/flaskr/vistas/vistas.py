from email import message
import os
from flask import request
from ..modelos import db, Usuario, UsuarioSchema, TareaSchema, Tarea
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
from ..tareas import convert_file


usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()


class VistaFile(Resource):
    def get(self):
        return "ok"


class VistaTareas(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = Usuario.query.filter_by(correo=identity).first()
        return [tarea_schema.dump(tarea) for tarea in Tarea.query.filter_by(usuario_id=user.id)]

    @jwt_required()
    def post(self):
        try:
            identity = get_jwt_identity()
            print("indetity", identity)
            user = Usuario.query.filter_by(correo=identity).first()
            file = request.files['fileName']
            filename = secure_filename(file.filename)
            nueva_tarea = Tarea(url_origen=request.url.replace("tasks", "files/") + filename,
                                formato_nuevo=request.form["newFormat"], usuario_id=user.id)
            db.session.add(nueva_tarea)
            db.session.commit()
            os.makedirs(f"{os.getenv('APP_FOLDER')}/flaskr/media/{user.id}", exist_ok=True)
            file.save(os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media/{user.id}", filename))
            convert_file.delay(nueva_tarea.id)

            return tarea_schema.dump(nueva_tarea)
        except Exception as e:
            return {"mensaje": f"{e.args.__str__}"}, 500


class VistaTarea(Resource):
    @jwt_required()
    def get(self, id_task):
        tarea = Tarea.query.get(id_task)
        if tarea is None:
            return {"mensaje": "No existe la tarea con id {}".format(str(id_task))}, 404
        return tarea_schema.dump(tarea)

    @jwt_required()
    def put(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        filenameDestino = tarea.url_destino.split('/')[-1]
        tarea.formato_nuevo = request.json.get("newFormat", tarea.formato_nuevo)
        status = tarea.status
        if (status != "uploaded"):
            tarea.status = "uploaded"
            tarea.url_destino = ""
            os.remove(os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media", filenameDestino))
        db.session.commit()
        if (status != "uploaded"):
            convert_file.delay(tarea.id)
        return tarea_schema.dump(tarea)

    @jwt_required()
    def delete(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        filenameOrigen = tarea.url_origen.split('/')[-1]
        filenameDestino = tarea.url_destino.split('/')[-1]
        if (tarea.status == "processed"):
            db.session.delete(tarea)
            db.session.commit()
            os.remove(os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media", filenameOrigen))
            os.remove(os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media", filenameDestino))
        return '', 204


class VistaLogIn(Resource):
    def post(self):
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(
            correo=correo, contrasena=contrasena).all()
        if usuario:
            token_de_acceso = create_access_token(identity=usuario[0].correo)
            return {'mensaje': 'Inicio de sesión exitoso', "token": token_de_acceso}
        else:
            return {'mensaje': 'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):

    def post(self):
        if len(Usuario.query.filter_by(correo=request.json["correo"]).all()) == 0:
            nuevo_usuario = Usuario(
                usuario=request.json["usuario"], correo=request.json["correo"], contrasena=request.json["contrasena"])
            token_de_acceso = create_access_token(
                identity=request.json["correo"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": 'Usuario creado exitosamente', "token_de_acceso": token_de_acceso}
        else:
            return ({"mensaje": 'Ya existe una cuenta con este correo electrónico'}, 400)
