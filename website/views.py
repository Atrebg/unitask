# main url per far funzionare il tutto. All the routes are defined here (blueprints allows us)
# min 14

from flask import Blueprint, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from . import db
from models import *
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])  # 17,14 views is the name of our blueprint (/ is the main page, this function will run
@login_required  # every time we go to the home page
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if len(title) < 1:
            flash('Title is too short!', category='error')
        else:
            new_offer = Offer(title=title, description = description ,id_user=current_user.id)
            db.session.add(new_offer)
            db.session.commit()
            flash('Task posted!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})