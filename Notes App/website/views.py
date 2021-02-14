# Store standard roots for website => home page, login page, sign up page, etc.
# this file is a blueprint of application i.e. has lot of urls/roots defined in it
# seperate app out so that views can be defined in multiple files
# render_template => render the html file

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# whenever we go to the '/' decorator => call the homepage function
@views.route('/', methods=['GET', 'POST'])

# current_user => gives all the information about the user who is logged in
# if user not logged in => anonymous user and not currently authenticated

# Cannot get to the homepage unless you are logged in
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note)<1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note added!', category='success')

    # in the home template => we can reference the 'current_user' and check if it is authenticated
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_node():
    note = json.loads(request.data)          # Take the request data which is a string => convert in into dictionary object
    noteId = note['noteId']                  # access noteId
    note = Note.query.get(noteId)            # look for the note that has that ID

    # if note exists
    if note:
        if note.user_id == current_user.id:   # if the user who is signed in owns the note
            db.session.delete(note)           # delete the note
            db.session.commit()               # return empty response

    return jsonify({})
