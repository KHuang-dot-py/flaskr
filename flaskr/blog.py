from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required # getting login_required wrapper code to use with views (redirects to login if no user)
from flaskr.db import get_db # getting connection to db

bp = Blueprint('blog', __name__)

# index homepage view
@bp.route('/')
def index():
    db = get_db()
    # gets all posts, this is a main feed
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# create view

@bp.route('/create', methods=('GET', 'POST'))
@login_required # user must be logged in to access these views, or else they are redirected to login.
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author = True):
    '''
    Get and return a post from the db
    
    :param id: post id
    :param check_author: optionally check if viewer is author
    '''
    db = get_db
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        'FROM post p join user ON p.author_id = user.id'
        'WHERE p.id = ?',
        (id,) # single-element tuple
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403) #403 means forbidden, as you are not the author

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    # implicit return update template for get request
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))