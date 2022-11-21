from email import message
import os
from flask import request
from ..modelos import db, Usuario, UsuarioSchema, TareaSchema, Tarea
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
import requests
from mimetypes import guess_type

from google.cloud import storage
from google.cloud import pubsub_v1

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
            # Consultar usuario que relizó la solicitud
            identity = get_jwt_identity()
            user = Usuario.query.filter_by(correo=identity).first()
            # Traer archivo y sus propiedades del request
            file = request.files['fileName']
            filename = secure_filename(file.filename)
            content = file.read()
            contentType = guess_type(filename)[0]
            # Subir archivo a cloud storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(os.getenv('BUCKET'))
            blob = bucket.blob(f"{identity}/{filename}")
            blob.upload_from_string(content, content_type=contentType)
            # Crear la tarea a la base de datos
            nueva_tarea = Tarea(url_origen=request.url.replace("tasks", "files/") + filename,
                                formato_nuevo=request.form["newFormat"], usuario_id=user.id)
            db.session.add(nueva_tarea)
            db.session.commit()
            # os.makedirs(f"{os.getenv('APP_FOLDER')}/flaskr/media/{user.id}", exist_ok=True)
            # file.save(os.path.join(f"{os.getenv('APP_FOLDER')}/flaskr/media/{user.id}", filename))
            # convert_file.delay(nueva_tarea.id)
            # Enviar la tarea a la cola de mensajes
            # requests.get(f"{os.getenv('WORKER')}/api/tasks/{nueva_tarea.id}")
            # Response de la solicitud con los datos de la tarea creada
            # Cloud pub/sub
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(os.getenv('PROJECT_ID'), os.getenv('TOPIC'))
            data = str(nueva_tarea.id).encode("utf-8")
            future = publisher.publish(topic_path, data)
            print(future.result())
            # Response
            return tarea_schema.dump(nueva_tarea)
        except Exception as e:
            return {"mensaje": f"{e}"}, 500


class VistaTarea(Resource):
    @jwt_required()
    def get(self, id_task):
        tarea = Tarea.query.get(id_task)
        if tarea is None:
            return {"mensaje": "No existe la tarea con id {}".format(str(id_task))}, 404
        return tarea_schema.dump(tarea)

    @jwt_required()
    def put(self, id_task):
        # Consultar usuario que realizo la solicitud
        identity = get_jwt_identity()
        user = Usuario.query.filter_by(correo=identity).first()
        # Consultar tarea
        tarea = Tarea.query.get_or_404(id_task)
        # Varaibles locales archivo
        filenameDestino = tarea.url_destino.split('/')[-1]
        tarea.formato_nuevo = request.json.get("newFormat", tarea.formato_nuevo)
        status = tarea.status
        # Logica update
        if (status != "uploaded"):
            tarea.status = "uploaded"
            tarea.url_destino = ""
            # Borrar de cloud storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(os.getenv("BUCKET"))
            blob = bucket.blob(f"{user.correo}/{filenameDestino}")
            blob.delete()
        db.session.commit()
        # Logica enivo a cola
        if (status != "uploaded"):
            # Cloud pub/sub
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(os.getenv('PROJECT_ID'), os.getenv('TOPIC'))
            data = str(tarea.id).encode("utf-8")
            future = publisher.publish(topic_path, data)
            print(future.result())
        # Response
        return tarea_schema.dump(tarea)

    @jwt_required()
    def delete(self, id_task):
        # Consultar usuario que realizo la solicitud
        identity = get_jwt_identity()
        user = Usuario.query.filter_by(correo=identity).first()
        # Consultar tarea
        tarea = Tarea.query.get_or_404(id_task)
        filenameOrigen = tarea.url_origen.split('/')[-1]
        filenameDestino = tarea.url_destino.split('/')[-1]
        if (tarea.status == "processed"):
            db.session.delete(tarea)
            db.session.commit()
            # Borrar de cloud storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(os.getenv("BUCKET"))
            blob = bucket.blob(f"{user.correo}/{filenameOrigen}")
            blob2 = bucket.blob(f"{user.correo}/{filenameDestino}")
            blob.delete()
            blob2.delete()
        return '', 200


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
