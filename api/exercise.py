from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from model.exercises import ExerciseModel
import json

exercise_api = Blueprint('exercise_api', __name__, url_prefix='/api/exercise')
api = Api(exercise_api)

# Initialize CORS for the exercise API blueprint
CORS(exercise_api)

class ExerciseLike(Resource):
    def post(self, exercise_id):
        # Find exercise by ID
        exercise = ExerciseModel.query.filter_by(id=exercise_id).first()

        if not exercise:
            return {'error': 'Exercise not found'}, 404

        # Increment likes for the exercise
        exercise.increase_likes()

        # Return JSON response
        return {'message': 'Exercise liked successfully'}, 200

class ExerciseRecords(Resource):
    def get(self):
        # Retrieve all exercise records from the database
        exercises = ExerciseModel.query.all()
        
        # Convert exercise records to JSON-ready format
        json_ready = [{'id': exercise.id, 'name': exercise.name, 'intensity': exercise.intensity,
                       'type': exercise.type, 'calories_burned': exercise.calories_burned,
                       'likes': exercise.likes} for exercise in exercises]
        
        # Return JSON response
        return jsonify(json_ready)

api.add_resource(ExerciseLike, '/like/<int:exercise_id>')
api.add_resource(ExerciseRecords, '/records')

# Initialize the exercise model
def init_exercise_model():
    ExerciseModel.load_data_from_csv('exercise_dataset.csv')

# This block is executed when running the file directly
if __name__ == "__main__":
    init_exercise_model()

    # Import app instance from __init__.py
    from __init__ import app

    # Register the exercise_api blueprint with the app
    app.register_blueprint(exercise_api)

    # Run the Flask application with debug mode enabled
    app.run(debug=True)
