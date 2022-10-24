from flask.cli import FlaskGroup

from flaskr import app
from flaskr.modelos import db, Usuario

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Usuario(usuario="daniel", correo="daniel.perez.ceron@gmail.com", contrasena="12345"))
    db.session.commit()


if __name__ == "__main__":
    cli()
