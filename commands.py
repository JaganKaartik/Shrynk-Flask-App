import click
from flask.cli import with_appcontext

from shrynk import db
from shynk.models import User,Dashboard

@click.command(name='create_tables')
@with_appcontext
def create_tables():
     db.create_all()