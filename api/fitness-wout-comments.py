from flask import Flask, Blueprint, request, jsonify, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
from model.sleeps import Sleep
from model.fitnesses import FitnessModel

app = Flask(__name__)
CORS(app)

sleep_api = Blueprint('sleep_api', __name__, url_prefix='/api/sleeps')
fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')

api_sleep = Api(sleep_api)
api_fitness = Api(fitness_api)

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad Request: Invalid input provided.'}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found: The requested resource could not be found.'}), 404

class SleepCRUD(Resource):
    def post(self):
        body = request.get_json()
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
        if stress_level is none:
            return {'message': 'Stress Level is missing'}, 400
        bmi_category = body.get('BMI Category')
        if bmi_category is none:
            return {'message': 'BMI Category is missing'}, 400
        blood_pressure = body.get('Blood Pressure')
        if blood_pressure is none:
            return {'message': 'Blood Pressure is missing'}, 400
        heart_rate = body.get('Heart Rate')
        if heart_rate is none:
            return {'message': 'Heart Rate is missing'}, 400
        daily_steps = body.get('Daily Steps')
        if daily_steps is none:
            return {'message': 'Daily Steps is missing'}, 400
        sleep_disorder = body.get('Sleep Disorder')
        if not all(field in body for field in required_fields):
            return jsonify({'error': 'Invalid input. Please provide all required fields.'}), 400
        new_sleep = Sleep(**body)
        created_sleep = new_sleep.create()
        if created_sleep:
            return jsonify(created_sleep.read()), 201
        else:
            return jsonify({'error': 'Failed to add record to the database.'}), 400

    def get(self):
        sleeps = Sleep.query.all()
        json_ready = [sleep.read() for sleep in sleeps]
        return jsonify(json_ready)

    def delete(self):
        body = request.get_json()
        del_id = body.get('id')
        result = Sleep.query.filter(Sleep._id == del_id).first()
        if result is none:
            return {'message': f'Sleep record with ID {del_id} not found'}, 404
        else:
            result.delete()
            return '', 204

api_sleep.add_resource(SleepCRUD, '/')

class FitnessPredict(Resource):
    def post(self):
        exercise_data = request.json
        if exercise_data is none:
            return jsonify({'error': 'No input data provided'}), 400
        fitness_model = FitnessModel.get_instance()
        predicted_calories = fitness_model.predict(exercise_data)
        return jsonify({'predicted_calories': predicted_calories})

api_fitness.add_resource(FitnessPredict, '/predict')

app.register_blueprint(sleep_api)
app.register_blueprint(fitness_api)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    FitnessModel.load_data_from_csv('fitness.csv')
    FitnessModel.train_model()
    app.run(debug=True, host="127.0.0.1", port=8080)
