import os
from flaskr.db import get_db

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")