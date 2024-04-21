from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.fitnesses import FitnessModel

fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')
api = Api(fitness_api)

# Initialize CORS for the fitness API blueprint
CORS(fitness_api)

class FitnessPredict(Resource):
    def post(self):
        data = request.get_json()

        duration = data.get('duration')
        bpm = data.get('bpm')
        intensity = data.get('intensity')

        if duration is None or bpm is None or intensity is None:
            return jsonify({'error': 'Invalid input. Please provide all required fields.'}), 400

        FitnessModel.load_data_from_csv('fitness.csv')
        FitnessModel.train_model()

        predicted_calories = FitnessModel.predict_calories(duration, bpm, intensity)

        return jsonify({'predicted_calories': predicted_calories}), 200

api.add_resource(FitnessPredict, '/predict')

def init_fitness_model():
    FitnessModel.load_data_from_csv('fitness.csv')
    FitnessModel.train_model()

# This block is executed when running the file directly
if __name__ == "__main__":
    init_fitness_model()

    # Import app instance from __init__.py
    from __init__ import app

    # Register the fitness_api blueprint with the app
    app.register_blueprint(fitness_api)

    # Run the Flask application with debug mode enabled
    app.run(debug=True)
