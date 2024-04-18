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
        def post(self):
            body = request.get_json()

            # Get data from the request body
            gender = body.get('Gender')
            if gender is None:
                return {'message': 'Gender is missing'}, 400

            age = body.get('Age')
            if age is None:
                return {'message': 'Age is missing'}, 400

            occupation = body.get('Occupation')
            if occupation is None:
                return {'message': 'Occupation is missing'}, 400

            sleep_duration = body.get('Sleep Duration')
            if sleep_duration is None:
                return {'message': 'Sleep Duration is missing'}, 400

            quality_of_sleep = body.get('Quality of Sleep')
            if quality_of_sleep is None:
                return {'message': 'Quality of Sleep is missing'}, 400

            physical_activity_level = body.get('Physical Activity Level')
            if physical_activity_level is None:
                return {'message': 'Physical Activity Level is missing'}, 400

            stress_level = body.get('Stress Level')
            if stress_level is None:
                return {'message': 'Stress Level is missing'}, 400

            bmi_category = body.get('BMI Category')
            if bmi_category is None:
                return {'message': 'BMI Category is missing'}, 400

            blood_pressure = body.get('Blood Pressure')
            if blood_pressure is None:
                return {'message': 'Blood Pressure is missing'}, 400

            heart_rate = body.get('Heart Rate')
            if heart_rate is None:
                return {'message': 'Heart Rate is missing'}, 400

            daily_steps = body.get('Daily Steps')
            if daily_steps is None:
                return {'message': 'Daily Steps is missing'}, 400

            sleep_disorder = body.get('Sleep Disorder')

            # Create a new person object
            new_person = Sleep(
                gender=gender,
                age=age,
                occupation=occupation,
                sleep_duration=sleep_duration,
                quality_of_sleep=quality_of_sleep,
                physical_activity_level=physical_activity_level,
                stress_level=stress_level,
                bmi_category=bmi_category,
                blood_pressure=blood_pressure,
                heart_rate=heart_rate,
                daily_steps=daily_steps,
                sleep_disorder=sleep_disorder
            )


            # Add person to the database
            just_added_person = new_person.create()

            # Check if person was successfully added to the database
            if just_added_person:
                # Return JSON representation of the added person
                return jsonify(just_added_person.read()), 200
            else:
                # Return an error message if the person could not be added to the database
                return {'message': 'Failed to add person to the database'}, 400
            pass

        def get(self): # Read Method
            # Retrieve all sleep records from the database
            sleeps = Sleep.query.all()
            
            # Convert sleep records to JSON-ready format
            json_ready = [sleep.read() for sleep in sleeps]
            
            # Return JSON response
            return jsonify(json_ready)
            pass

        def delete(self):  # Delete method
            ''' Find sleep by ID '''
            body = request.get_json()
            del_id = body.get('id')  # Assuming 'id' is used to specify the sleep record to delete
            result = Sleep.query.filter(Sleep._id == del_id).first()
            if result is None:
                return {'message': f'Sleep record with ID {del_id} not found'}, 404
            else:
                result.delete()
                print("delete")
            pass

    class _get(Resource):
        def get(self, lname=None):
            if lname is not None:
                # Filter sleep records by lname
                filtered_sleeps = Sleep.query.filter_by(lname=lname).all()
                if filtered_sleeps:
                    # Convert filtered sleep records to JSON-ready format
                    json_ready = [sleep.read() for sleep in filtered_sleeps]
                    return jsonify(json_ready), 200
                else:
                    return {'message': 'No sleep records found for the specified lname'}, 404
            else:
                # Retrieve all sleep records from the database if no lname is specified
                sleeps = Sleep.query.all()
                json_ready = [sleep.read() for sleep in sleeps]
                return jsonify(json_ready), 200
            
    class SleepByDuration(Resource):
        def get(self):
            # Parse query parameters
            parser = reqparse.RequestParser()
            parser.add_argument('sleep_duration', type=float, required=True, help='Sleep duration is required')
            args = parser.parse_args()
            
            # Get sleep duration from query parameters
            sleep_duration = args['sleep_duration']

            # Filter sleep data by duration
            filtered_sleeps = Sleep.query.filter_by(sleep_duration=sleep_duration).all()

            # Convert filtered sleep data to JSON format
            json_ready = [sleep.read() for sleep in filtered_sleeps]

            return jsonify(json_ready)
    
    api.add_resource(_CRUD, '/')
    api.add_resource(_get, '/<string:lname>')
    api.add_resource(SleepByDuration, '/duration/<float:sleep_duration>')

app.register_blueprint(sleep_api)


if __name__ == '__main__':
    app.run(debug=True)