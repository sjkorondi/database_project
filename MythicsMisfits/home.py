from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from MythicsMisfits.auth import login_required
from MythicsMisfits.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    db = get_db()
    chars = db.execute(
        'SELECT * FROM characters'
        ' ORDER BY character_name ASC'
    ).fetchall()
    return render_template('home/index.html', chars=chars)