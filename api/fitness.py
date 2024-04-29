# this code was based on ChatGPT
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from model.sleeps import Sleep
from model.fitnesses import FitnessModel
from sqlalchemy.exc import SQLAlchemyError, OperationalError


# Initialize the Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create blueprints for sleep and fitness APIs
sleep_api = Blueprint('sleep_api', __name__, url_prefix='/api/sleeps')
fitness_api = Blueprint('fitness_api', __name__, url_prefix='/api/fitness')

# Initialize RESTful APIs
api_sleep = Api(sleep_api)
api_fitness = Api(fitness_api)

# Error handling for HTTP 400 and 404
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad Request: Invalid input provided.'}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found: The requested resource could not be found.'}), 404

# Sleep API Resource class
class SleepCRUD(Resource):
    def get(self):
        try:
            # Query all sleep records from the database
            sleeps = Sleep.query.all()
            
            # Convert the sleep records to JSON-ready format using the `read` method
            json_ready = [sleep.read() for sleep in sleeps]
            
            # Return the JSON response containing the list of sleep records
            return jsonify(json_ready)
        
        # Handle database connection errors
        except OperationalError as db_error:
            return jsonify({'error': f'Database connection error: {str(db_error)}'}), 500
        
        # Handle query execution errors (e.g., syntax or data access issues)
        except SQLAlchemyError as query_error:
            return jsonify({'error': f'Query error: {str(query_error)}'}), 500
        
        # Handle data format errors (e.g., JSON conversion issues)
        except json.JSONDecodeError as json_error:
            return jsonify({'error': f'Data format error: {str(json_error)}'}), 400
        
        # Handle any other unexpected errors
        except Exception as error:
            return jsonify({'error': f'An unexpected error occurred: {str(error)}'}), 500

# Add SleepCRUD resource to sleep API
api_sleep.add_resource(SleepCRUD, '/')

# Fitness API Resource class
class FitnessPredict(Resource):
    def post(self):
        """Endpoint to predict calorie burn based on exercise data."""
        # Get exercise data from the request
        exercise_data = request.json

        # Check if the request body is missing
        if exercise_data is None:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Get instance of FitnessModel
        fitness_model = FitnessModel.get_instance()
        
        # Predict calorie burn
        predicted_calories = fitness_model.predict(exercise_data)

        # Return predicted calorie burn as JSON response
        return jsonify({'predicted_calories': predicted_calories})

# Add FitnessPredict resource to fitness API
api_fitness.add_resource(FitnessPredict, '/predict')

# Register sleep and fitness API blueprints with the main app
app.register_blueprint(sleep_api)
app.register_blueprint(fitness_api)

# Define index route
@app.route('/')
def index():
    return render_template("index.html")

# Main block to initialize the application and run the server
if __name__ == "__main__":
    # Initialize and train fitness model
    FitnessModel.load_data_from_csv('fitness.csv')
    FitnessModel.train_model()

    # Run the Flask application
    app.run(debug=True, host="127.0.0.1", port=8080)
