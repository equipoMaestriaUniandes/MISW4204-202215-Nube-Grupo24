import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum


db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True


class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_origen = db.Column(db.String(1000))
    url_destino = db.Column(db.String(1000), default='')
    formato_nuevo = db.Column(db.String(50))
    time_stamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class TareaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tarea
        include_relationships = True
        load_instance = True
