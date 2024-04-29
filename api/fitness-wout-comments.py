from flask import Flask, Blueprint, request, jsonify, render_template, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.sleeps import Sleep
from model.fitnesses import FitnessModel
from sqlalchemy.exc import SQLAlchemyError, OperationalError


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

    def get(self):
        try:
            sleeps = Sleep.query.all()
            json_ready = [sleep.read() for sleep in sleeps]
            return jsonify(json_ready)
        except OperationalError as db_error:
            return jsonify({'error': f'Database connection error: {str(db_error)}'}), 500
        except SQLAlchemyError as query_error:
            return jsonify({'error': f'Query error: {str(query_error)}'}), 500
        except json.JSONDecodeError as json_error:
            return jsonify({'error': f'Data format error: {str(json_error)}'}), 400
        except Exception as error:
            return jsonify({'error': f'An unexpected error occurred: {str(error)}'}), 500



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
