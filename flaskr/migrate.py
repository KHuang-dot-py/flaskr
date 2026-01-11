import os
from flaskr.db import get_db

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")

def get_current_version(db):
    return db.execute(
        "SELECT version FROM schema_version"
    ).fetchone()[0] # should only be one value in there anyways

def set_version(db, version):
    db.execute(
        "UPDATE schema_version SET version = ?", (version,)
    )

def run_migrations():
    db = get_db()
    current_version = get_current_version(db)
    # applied = [int]
    # get list of migration sql schema files
    migrations = sorted(
        f for f in os.listdir(MIGRATIONS_DIR)
        if f.endswith(".sql")
    )

    for fname in migrations:
        version = int(fname.split("_")[0])
        if version > current_version:
            with open(os.path.join(MIGRATIONS_DIR, fname)) as f:
                db.executescript(f.read())
            set_version(db, version)
            # applied.append(version)
    db.commit()
    # print("Migrations completed:", applied)