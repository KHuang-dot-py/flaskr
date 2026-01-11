import click
from flask import current_app

@click.command("migrate")
def migrate_command():
    """Run database migrations."""
    click.echo("Running migrations")
    from flaskr.migrate import run_migrations
    run_migrations()
    click.echo("Migrations completed")