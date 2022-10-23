import os
from flask import request, redirect, url_for
from ..modelos import db, Usuario, UsuarioSchema, TareaSchema, Tarea
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.utils import secure_filename
import pathlib
from ..tareas import add_together, convert_file
UPLOAD_FOLDER = 'uploads'
usuario_schema = UsuarioSchema()
tarea_schema = TareaSchema()


class VistaFile(Resource):
    def get(self):
        return "ok"


class VistaTareas(Resource):
    @jwt_required()
    def get(self):
        return [tarea_schema.dump(tarea)
                for tarea in Tarea.query.filter()]

    def post(self):
        import pdb
        # pdb.set_trace()
        file = request.files['fileName']
        filename = secure_filename(file.filename)
        work_path = pathlib.Path().resolve()
        filepath = os.path.join(work_path, UPLOAD_FOLDER, filename)
        file.save(filepath)
        nueva_tarea = Tarea(url_origen=request.url.replace("tasks", "files/")+filename,
                            formato_nuevo=request.form["newFormat"])
        db.session.add(nueva_tarea)
        db.session.commit()
        convert_file.delay(
            nueva_tarea.id, filename, request.form["newFormat"], request.url.replace("tasks", "files/"))

        return tarea_schema.dump(nueva_tarea)


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
        tarea.formato_nuevo = request.json.get(
            "newFormat", tarea.formato_nuevo)
        tarea.status = "uploaded"
        db.session.commit()
        return tarea_schema.dump(tarea)

    @jwt_required()
    def delete(self, id_task):
        tarea = Tarea.query.get_or_404(id_task)
        db.session.delete(tarea)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):
    def post(self):
        add_together.delay(23, 42)
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]
        usuario = Usuario.query.filter_by(
            correo=correo, contrasena=contrasena).all()
        if usuario:
            token_de_acceso = create_access_token(identity=usuario[0].id)
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
