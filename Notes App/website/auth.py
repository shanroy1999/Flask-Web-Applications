# Auth blueprint => contains login, logout, sign up

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

# password hash => way to secure password such that it is never in plain text
# hashing function => one-way function such that it does not have an inverse => has no inverse
# f(password) -> encrypted password but f(encrypted) -> cannot find the original password

auth = Blueprint('auth', __name__)

# Jinga => allows to pass variables/values inside the template and use them in the html file

""" routes => need to know the type of request they will accept => GET / POST / PUT
    By default => route accept only GET request => need to specify other requests in the function
GET request => loading webpage, retrieving information
POST request => some kind of change to the database / state of the system
            => Sign Up Page => form method is "POST" => send a "POST" request to the url "signup"
            => Post request has all the information - firsname, email, password => sent to server
            => Server interprets the information and respond based on that post request
"""

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method=='POST':

        # get the information entered by the user on the login page
        email = request.form.get('email')
        password = request.form.get('password')

        # query the database and look for the specific entry to check if the user exists in database
        # .first() => return the first email
        user = User.query.filter_by(email=email).first()

        # if we find the user
        if user:
            # check if the password typed is equal to the hash stored on the server
            # Compare the hashes of password entered and password stored
            if check_password_hash(user.password, password):
                flash('Logged in Successfully', category='success')

                # remember the fact that user is logged in unless user clear history or server shuts down
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password entered, try again', category='error')
        else:
            flash('Email ID does not exist', category='error')

    # when we render html in flask => we call it a template
    # Jinga => special template language to use with flask => allows to write python in html docs
    return render_template("login.html", user=current_user)

@auth.route('/logout')

# Make sure that we cannot logout unless we are logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Get the information sent in the form
    Whenever we access 'request' variable inside the root => it will have information of about request
    that we sent to access the route

    request.form => access the form attribute of the request => has all data sent as part of form
                 => immutable dict object => [('email', 'xyz@abc.com'), ['password', 'qwert']]
    """
    # if it is a post request => get all the information from the form => email, firstname, pass1, pass2
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if the email id of user already exists in database while signup
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        # Make sure the information in the form is valid
        elif len(email)<4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName)<2:
            flash('FirstName must be greater than 2 characters', category='error')
        elif password1!=password2:
            flash('Passwords dont match', category='error')
        elif len(password1)<7:
            flash('Passwords must be atleast 7 characters', category='error')
        else:
            # Create a new user using the User class defined in 'models.py'
            new_user = User(email=email, firstName=firstName,
                            password=generate_password_hash(password1, method='sha256'))
                            # sha256 -> hashing method

            # add the newly created user to the database
            db.session.add(new_user)

            # Make a commit to the database => since we have created some changes to db => update db
            db.session.commit()

            login_user(new_user, remember=True)

            # Flash the account created message on successfully adding user to the database
            flash('Account Created Successfully!', category='success')

            # After creation of account => need to sign-in => redirect to home page
            # return redirect for the url of home page
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
