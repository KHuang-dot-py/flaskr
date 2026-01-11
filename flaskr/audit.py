from flask import g
from flaskr.db import get_db

def log_event(action, entity_type, entity_id)