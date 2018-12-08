#-*- coding:utf-8 -*-
import click
from sqlalchemy_utils import database_exists, create_database

from dataton_anticorrupcion.app import create_app
from dataton_anticorrupcion.extensions import db, pwd_context
from dataton_anticorrupcion.blueprints.usuarios.models import Usuarios


# Create an app context for the database connection
app = create_app()
db.app = app


@click.group()
def cli():
    pass


@click.command()
@click.option('--with-testdb/--no-with-testdb',
              default=False,
              help='Create a test db too?')
def init(with_testdb):
    db.drop_all()
    db.create_all()
    if with_testdb:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])
        if not database_exists(db_uri):
            create_database(db_uri)
    click.echo('Init.')


@click.command()
def seed():
    usuarios = [
        {
            'rol': 'admin',
            'nombre': u'Guillermo Valdés Lozano',
            'email': 'guillermo.valdes@seacoahuila.org.mx',
            'contrasena': pwd_context.hash("cetujavu"),
        },
    ]
    for us in usuarios:
        Usuarios(**us).save()
        click.echo('Seed user: {0}.'.format(us['email']))


@click.command()
@click.option('--with-testdb/--no-with-testdb',
              default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_testdb):
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(seed)


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
