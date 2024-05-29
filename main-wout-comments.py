import threading

from flask import render_template, request
from flask.cli import AppGroup
from __init__ import app, db, cors
from flask_cors import CORS
from api.covid import covid_api
from api.joke import joke_api
from api.user import user_api
from api.player import player_api
from api.titanic import titanic_api
from api.fitness import fitness_api, sleep_api
from model.users import initUsers
from model.players import initPlayers
from model.titanicML import initTitanic
from model.fitnesses import initFitnessModel
from model.journal import initMessages
from model.sleeps import init_sleep
from projects.projects import app_projects

db.init_app(app)
CORS(app)
app.register_blueprint(joke_api)
app.register_blueprint(covid_api)
app.register_blueprint(user_api)
app.register_blueprint(player_api)
app.register_blueprint(titanic_api)
app.register_blueprint(app_projects)
app.register_blueprint(fitness_api)
app.register_blueprint(sleep_api)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

custom_cli = AppGroup('custom', help='Custom commands')

@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()
    initTitanic()
    initFitnessModel()
    initMessages()
    init_sleep()

app.cli.add_command(custom_cli)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port="8080")
