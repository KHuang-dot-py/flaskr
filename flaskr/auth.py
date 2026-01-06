# BLUEPRINTS NOTES:
# Blueprints prevent factories from getting messy by letting you define routes and logic outside the factory, 
# keeping the factory focused on setup and registration rather than every single view, 
# which also avoids circular imports and improves modularity.

# Factory as construction site manager: blueprints are work done by each team, then just put together by the manager


import functools
    
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#This creates a Blueprint named 'auth', url prefix will be prepended to all URLs associated
# The blueprint needs to know where it’s defined, 
# so __name__ is passed (evaluates to the name of the current module)

bp = Blueprint('auth', __name__, url_prefix='/auth')

# ------ Registration ------

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # execute method executes SQL code in SQLite, while preventing injection attack
                # ? parameter placeholder tells SQLite to not treat them as SQL code, and that
                # values will be passed separately
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # transaction ends, and changes are written to disk
                db.commit()
            # non-unique user, shows validation error to user
            except db.IntegrityError:
                error = f"User {username} is already registered."
            # successful login, redirect
            else:
                # generate URL based on name of login view
                return redirect(url_for("auth.login"))
        # stores messages that can be retrieved when rendering template
        flash(error)

    return render_template('auth/register.html')

# ------ Login ------

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # gets first row from query results
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # returns a row object

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is info stored as a cookie on browser (in flask). Without clearing:
            # Old session data could leak across users, or malicious data left
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index')) # this module might be imported into somewhere that index is defined...

        flash(error)

    return render_template('auth/login.html')

# ------
# defines a function that runs before any request.
@bp.before_app_request
def load_logged_in_user():
    # gets id from session if it exist. None by default
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # loads user data from db and stores it in g.user for the duration of the request.
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# Logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# decorator for views that require login

def login_required(view):
    # functools.wraps(view) copies critical metadata from the original view function onto the wrapper-
    # -so Flask can route, introspect, debug, and generate URLs correctly.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

