import sqlite3
from datetime import datetime

import click
from flask import current_app, g

# current app is a context-local proxy, 
# it points to and supplies the app handling the current request at runtime

def get_db():
    # g is a context-local proxy that can stores values for the duration of the current request
    # cleared automatically afterwards by flask
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # allows access of each sqlite row as a dictionary
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # get database connection
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # executing our sql schema to create the tables
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# telling python how to interpret 'timestamp' values in the database
# here we are converting the value to a timestamp.timestamp
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    # tells flask to call that function when cleaning up after returning response
    app.teardown_appcontext(close_db)
    # add a new command that can be called with the flask command
    app.cli.add_command(init_db_command)