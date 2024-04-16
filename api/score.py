# Import necessary modules
from flask import Flask, request, jsonify
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building

# Create Flask app instance
score_api = Blueprint('score_api', __name__,
                   url_prefix='/api/score')


# Define a dictionary to store game scores
game_scores = {}

# Route to handle posting game scores
@score_api.route('/post_score', methods=['POST'])
def post_score():
    # Get data from the request body
    data = request.json
    
    # Extract game details from the data
    home_team = data.get('home_team')
    away_team = data.get('away_team')
    home_score = data.get('home_score')
    away_score = data.get('away_score')
    
    # Check if all required parameters are provided
    if not (home_team and away_team and home_score and away_score):
        return jsonify({'error': 'Missing required parameters.'}), 400
    
    # Store the game score
    game_id = len(game_scores) + 1
    game_scores[game_id] = {
        'home_team': home_team,
        'away_team': away_team,
        'home_score': home_score,
        'away_score': away_score
    }
    
    return jsonify({'message': 'Game score posted successfully.', 'game_id': game_id}), 201

# Route to get all game scores
@score_api.route('/game_scores', methods=['GET'])
def get_game_scores():
    return jsonify(game_scores)

# Route to delete a game score by ID
@score_api.route('/delete_score/<int:game_id>', methods=['DELETE'])
def delete_score(game_id):
    if game_id in game_scores:
        del game_scores[game_id]
        return jsonify({'message': f'Game score with ID {game_id} deleted successfully.'}), 200
    else:
        return jsonify({'error': f'Game score with ID {game_id} not found.'}), 404

# Run the Flask app
if __name__ == '__main__':
    score_api.run(debug=True)
