#this was teacher-provided code
import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization
from flask_cors import CORS
from __init__ import app, db, cors

# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
from api.titanic import titanic_api
from api.fitness import fitness_api
from api.CurrentChar import currentchar_api
from api.CharClass import classes_api
#from api.mental import mental_api
from api.fitness import sleep_api
# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.titanicML import initTitanic
from model.fitnesses import initFitnessModel
from model.CurrentChars import initCurrentChars
from model.classes import initCharClasses
from model.journal import initMessages
from model.sleeps import init_sleep

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)
CORS(app)
# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(titanic_api) # register api routes
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(fitness_api)
app.register_blueprint(currentchar_api)
app.register_blueprint(classes_api)
app.register_blueprint(sleep_api)

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()
    initTitanic()
    initFitnessModel()
    initCurrentChars()
    initCharClasses()
    initMessages()
    init_sleep()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="127.0.0.1", port="8080")
    
