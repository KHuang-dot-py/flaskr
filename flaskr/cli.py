import click
from flask import current_app

@click.command("migrate")
def migrate_command():
    """Run database migrations."""
    from flaskr.migrate import run_migrations
    run_migrations()