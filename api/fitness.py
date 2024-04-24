from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.fitnesses import FitnessModel
import json

fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')
api = Api(fitness_api)

# Initialize CORS for the fitness API blueprint
CORS(fitness_api)

class FitnessPredict(Resource):
    def post(self):
        print("hi")
        data = request.get_json()
        duration = data.get('Duration')
        bpm = data.get('BPM')
        intensity = data.get('Intensity')
        print(data)

        if duration is None or bpm is None or intensity is None:
            # json_temp = jsonify({'error': 'Invalid input. Please provide all required fields.'}), 400
            
            return json.dumps({'error': 'Invalid input. Please provide all required fields.'}), 400, {'Content-Type': 'application/json'}
        

        # Load data and train model (this should ideally be done during initialization)
        FitnessModel.load_data_from_csv('fitness.csv')
        FitnessModel.train_model()

        try:
            # Predict calories
            predicted_calories = FitnessModel.predict_calories(duration, bpm, intensity)
        except Exception as e:
            # return jsonify({'error': str(e)}), 500  # Handle prediction error
            return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}

        # Return JSON response with predicted calories
        # return jsonify({'predicted_calories': str(predicted_calories)}), 200
        response_data = {'predicted_calories': str(predicted_calories)}
        # return json.dumps(response_data), 200, {'Content-Type': 'application/json'}
        return jsonify(response_data)

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