# import from current package(ie 'website' folder) the db object
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# func => we dont need to specify date ourself, instead sqlalchemy take care of it
# whenever we create new note => func automatically adds the current date and time for that note

# define the database model => layout / blueprint of object stored in the database

# Tell the database that all the notes need to look like this
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))                          # Store the text for the notes
    date = db.Column(db.DateTime(timezone=True), default=func.now())      # Date the note was created at

    # associate note with the specific user
    # set relationship between note object and user object using a foreign key
    # store id of user who created the note
    # 1 user can have many notes => One-to-many relationship
    # 'user' => represents the 'User' class
    # 'user.id' => 'id' field of user object
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    # define schema / all the columns that we want to store in the database
    # for an object in database => need a primary key for each to uniquely identify each of the object
    # here => id is the primary key => unique identifier
    # id => automatically set by the database by default for a new object, no need to set manually
    # (id of new object) = (id of prev inserted obj) + 1
    # Store all the users in this schema

    id = db.Column(db.Integer, primary_key=True)      # define the type of the column
    email = db.Column(db.String(150), unique=True)    # 150 -> max length of string, no user can have duplicate
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))

    # need to access all the notes written by a user
    # tell SQLAlchemy that everytime we create a new note => add the note id into user-note relationship
    notes = db.relationship('Note')
