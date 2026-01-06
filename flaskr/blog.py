from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required # getting login_required wrapper code to use with views (redirects to login if no user)
from flaskr.db import get_db # getting connection to db

bp = Blueprint('blog', __name__)