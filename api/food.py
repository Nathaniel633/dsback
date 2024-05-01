from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.foods import FoodModel
import json

food_api = Blueprint('food_api', __name__, url_prefix='/api/food')
api = Api(food_api)

# Initialize CORS for the foodsAPI blueprint
CORS(food_api)

class FoodPredict(Resource):
    def post(self):
        # Data Extraction
        data = request.get_json()
        steps = data.get('Steps')
        stress = data.get('Stress')
        meditation = data.get('Meditation')
        # Data validation
        if steps is None or stress is None or meditation is None:
            return json.dumps({'error': 'Invalid input. Please provide all required fields.'}), 400, {'Content-Type': 'application/json'}

        # Load data and train model 
        FoodModel.load_data_from_csv('food.csv')
        FoodModel.train_model()

        try:
            # Predict produce
            predicted_produce = FoodModel.predict_produce(steps, stress, meditation)
        except Exception as e: # Error statement if needed
            return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}

        # Return JSON response with predicted produce
        response_data = {'predicted_produce': str(predicted_produce)}
        return jsonify(response_data)

api.add_resource(FoodPredict, '/predict')
# Establish api endpoint url

def init_food_model():
    FoodModel.load_data_from_csv('food.csv')
    FoodModel.train_model()

# This block is executed when running the file directly
if __name__ == "__main__":
    init_food_model()

    # Import app instance from __init__.py
    from __init__ import app

    # Register the food_api blueprint with the app
    app.register_blueprint(food_api)

    # Run the Flask application with debug mode enabled
    app.run(debug=True)