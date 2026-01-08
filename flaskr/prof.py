from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required # getting login_required wrapper code to use with views (redirects to login if no user)
from flaskr.db import get_db # getting connection to db

bp = Blueprint('prof', __name__, url_prefix= "/prof")

# getting posts soley by a single user
@bp.route('/<string:user>')
def profile(user):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u on p.author_id = u.id'
        ' WHERE u.id == (' \
        'SELECT id FROM user WHERE username = ?' \
        ')'
        ' ORDER BY created DESC',
        (user,)
    ).fetchall()
    return render_template('blog/feed/prof.html', posts = posts)