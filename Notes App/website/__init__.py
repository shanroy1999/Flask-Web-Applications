# __init__.py => converts the folder 'website' into a package to use in other python files

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# for storing information in a database
db = SQLAlchemy()                   # database object
DB_NAME = "database.db"             # database name

# Create flask application
def create_app():
    app = Flask(__name__)                           # __name__ => name of the file
    app.config['SECRET_KEY'] = 'jnsndijijfelmsan'   # encrypt/secure session data

    # Tell flask that the SQlite database is stored/located at this location
    # Store the database in the 'website' folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    # initialize the database with the flask app
    db.init_app(app)

    # tell flask that we have blueprints which contains views/urls for application
    from .views import views
    from .auth import auth

    # register blueprints with flask application
    # url_prefix => tells how to access the urls inside the bluprints file
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))          # similar to filter_by but here by default it will look for primary key
        # dont have to specify id=int(id)

    return app

# create database which were defined in 'models.py' file
def create_database(app):
    # check if the database already exists or not
    # if database does not exist => Create it
    # if database already exist => we will have to override it

    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)                      # which app we are creating database for
        print('Created database')
