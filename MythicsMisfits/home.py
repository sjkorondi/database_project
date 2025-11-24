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
    if g.user is None:
        return render_template('home/index.html', mychars=None, otherchars=None)
    mychars = db.execute(
        'SELECT * FROM characters '
        'WHERE user_id = ? '
        'ORDER BY character_name ASC', (g.user['user_id'],)).fetchall()
    otherchars = db.execute(
        'SELECT characters.*, users.username '
        'FROM characters JOIN users ON characters.user_id = users.user_id '
        'WHERE characters.user_id != ? '
        'ORDER BY characters.character_name ASC', (g.user['user_id'],)).fetchall()
    return render_template('home/index.html', mychars=mychars, otherchars=otherchars)

@bp.route('/items')
def items():
    db = get_db()
    items = db.execute(
        'SELECT * FROM items '
        'ORDER BY item_name ASC').fetchall()
    return render_template('home/items.html', items=items)

@bp.route('/quests')
def quests():
    db = get_db()
    quests = db.execute(
        'SELECT * FROM quests '
        'ORDER BY quest_id ASC').fetchall()
    return render_template('home/quests.html', quests=quests)

@bp.route('/classes')
def classes():
    db = get_db()
    classes = db.execute(
        'SELECT * FROM classes '
        'ORDER BY class_name ASC').fetchall()
    return render_template('home/classes.html', classes=classes)

@bp.route('/character/make', methods=('GET', 'POST'))
@login_required
def makecharacter():
    if request.method == 'POST':
        character_name = request.form['character_name']
        class_id = request.form['class_id']
        level = request.form['level']
        db = get_db()
        error = None

        if not character_name:
            error = 'Character name is required.'
        elif not class_id:
            error = 'Class ID is required.'
        elif not level or not level.isdigit() or int(level) < 1:
            error = 'Level must be a positive integer.'

        if error is None:
            db.execute(
                'INSERT INTO characters (character_name, class_id, level, user_id) '
                'VALUES (?, ?, ?, ?)',
                (character_name, class_id, int(level), g.user['user_id'])
            )
            db.commit()
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('home/makecharacter.html')

@bp.route('/character/<int:character_id>/edit', methods=('GET', 'POST'))
@login_required
def editcharacter(character_id):
    db = get_db()
    character = db.execute(
        'SELECT * FROM characters WHERE character_id = ?', (character_id,)
    ).fetchone()

    if character is None:
        abort(404, f"Character id {character_id} doesn't exist.")
    if character['user_id'] != g.user['user_id']:
        abort(403)

    quests = db.execute(
        'SELECT * FROM quests'
    ).fetchall()

    classes = db.execute(
        'SELECT * FROM classes'
    ).fetchall()

    if request.method == 'POST':
        print(request.form)
        character_name = request.form['character_name']
        class_id = request.form['class_id']
        level = request.form['level']
        quest = request.form['quest_id']
        error = None

        if not character_name:
            error = 'Character name is required.'
        elif not class_id:
            error = 'Class ID is required.'
        elif not level or not level.isdigit() or int(level) < 1:
            error = 'Level must be a positive integer.'
        elif not quest:
            error = 'Quest ID is required.'

        if error is None:
            db.execute(
                'UPDATE characters SET character_name = ?, class_id = ?, level = ?, quest_id = ? '
                'WHERE character_id = ?',
                (character_name, class_id, int(level), quest, character_id)
            )
            db.commit()
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('home/editcharacter.html', character=character, quests=quests, classes=classes)

@bp.route('/character/<int:character_id>/delete', methods=('POST',))
@login_required
def deletecharacter(character_id):
    db = get_db()
    character = db.execute(
        'SELECT * FROM characters WHERE character_id = ?', (character_id,)
    ).fetchone()

    if character is None:
        abort(404, f"Character id {character_id} doesn't exist.")
    if character['user_id'] != g.user['user_id']:
        abort(403)

    db.execute('DELETE FROM characters WHERE character_id = ?', (character_id,))
    db.commit()
    return redirect(url_for('home.index'))