import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.sleeps import Sleep

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

sleep_api = Blueprint('sleep_api', __name__, url_prefix='/api/sleeps')

api = Api(sleep_api)

class SleepApi:
    class _CRUD(Resource):

        def get(self): # Read Method
            # Retrieve all sleep records from the database
            sleeps = Sleep.query.all()
            
            # Convert sleep records to JSON-ready format
            json_ready = [sleep.read() for sleep in sleeps]
            
            # Return JSON response
            return jsonify(json_ready)
            pass
           


app.register_blueprint(sleep_api)


if __name__ == '__main__':
    app.run(debug=True)