from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.fitnesses import FitnessModel

fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')
api = Api(fitness_api)

class FitnessPredict(Resource):
    def post(self):
        """Endpoint to predict calorie burn based on exercise data."""
        # Get exercise data from the request
        exercise_data = request.json
        # Get instance of FitnessModel
        fitness_model = FitnessModel.get_instance()
        # Predict calorie burn
        predicted_calories = fitness_model.predict(exercise_data)
        # Return predicted calorie burn as JSON response
        return jsonify({'predicted_calories': predicted_calories})

api.add_resource(FitnessPredict, '/predict')

def init_fitness_model():
    """Initialize the FitnessModel."""
    FitnessModel.get_instance()

if __name__ == "__main__":
    init_fitness_model()
    fitness_api.run(debug=True)
