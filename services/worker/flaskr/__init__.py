from flask_restful import Api
from flask import Flask, send_from_directory, jsonify
import os

from .modelos import db, Usuario
from .tareas import convert_file
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_apscheduler import APScheduler

from google.cloud import pubsub_v1
from google.api_core import retry

app = Flask(__name__)
app.config.from_object("flaskr.config.Config")


app_context = app.app_context()
app_context.push()

db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)


@scheduler.task('interval', id='worker', seconds=1, misfire_grace_time=None)
def worker():
    with scheduler.app.app_context():
        print("tarea worker")
        # Capturar mensaje
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(os.getenv('PROJECT_ID'), os.getenv('SUB'))
        # Se suscribe
        with subscriber:
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": 1},
                retry=retry.Retry(deadline=300),
            )
            # Verifica los mensajes
            if len(response.received_messages) == 0:
                return
            # Procesa mensajes
            ack_ids = []
            for received_message in response.received_messages:
                print(f"Received: {received_message.message.data}.")
                convert_file(int(received_message.message.data))
                # received_message.ack_with_response()
                ack_ids.append(received_message.ack_id)
            # Acknowledges the received messages so they will not be sent again.
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )


@app.route("/")
def hello_world():
    return jsonify(hello="world")


api = Api(app)

jwt = JWTManager(app)

scheduler.start()
