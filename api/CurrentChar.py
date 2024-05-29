import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from __init__ import app, db
from model.CurrentChars import CurrentChar

currentchar_api = Blueprint('currentchar_api', __name__,
                   url_prefix='/api/currentchar')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(currentchar_api)

from flask import request, jsonify
from model.CurrentChars import CurrentChar

class CurrentCharAPI:        
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()  # Get the body of the request
            
            # Extracting data from the JSON body
            id = body.get('id')
            classname = body.get('classname', None)
            health = body.get('health', None)
            attack = body.get('attack', None)
            range = body.get('range', None)
            movement = body.get('movement', None)
            
            # Find the existing character by ID
            char = CurrentChar.query.filter_by(id=id).first()
            
            # If the character does not exist, return an error
            if not char:
                return jsonify({'message': 'Character not found'}), 404
            
            # Updating fields only if they are provided in the request
            if classname:
                char.classname = classname
            if health is not None:
                char.health = health
            if attack is not None:
                char.attack = attack
            if range is not None:
                char.range = range
            if movement is not None:
                char.movement = movement
            
            try:
                db.session.commit()  # Commit changes to the database
                return jsonify(char.read()), 200  # Return the updated character information
            except Exception as e:
                db.session.rollback()  # Rollback in case of error
                return jsonify({'message': 'Failed to update character', 'error': str(e)}), 500
            
        # @token_required
        def get(self): # Read Method
            CurrentCharacter = CurrentChar.query.all()    # read/extract all users from database
            json_ready = [CurrentCharacter.read() for CurrentCharacter in CurrentCharacter]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

        def put(self):
            body = request.get_json() # get the body of the request
            classname = body.get('classname')
            print(classname)
            health = body.get('health') # get the UID (Know what to reference)
            attack = body.get('attack') # get name (to change)
            range = body.get('range') # get name (to change)
            movement = body.get('movement') # get name (to change)
            # print(body)
            CurrentCharacter = CurrentChar.query.all() # get users
            print(CurrentCharacter)
            # for character in CurrentCharacter:
                # if character.classname == classname: # find user with matching uid
            # check length of current character todo
            
            if len(CurrentCharacter) < 1:
                print("Length of CurrentChars list from db is empty; no characters in database")
                return f"char of {classname} created; no Characters updated because none were found"
            else:
                CurrentCharacter[0].update(classname, health, attack, range==True, movement==True) # update info
                return f"char of {classname} created; {CurrentCharacter[0].read()} Updated"


    # class _Security(Resource):
    #     def post(self):
    #         try:
    #             body = request.get_json()
    #             if not body:
    #                 return {
    #                     "message": "Please provide user details",
    #                     "data": None,
    #                     "error": "Bad request"
    #                 }, 400
    #             ''' Get Data '''
    #             uid = body.get('uid')
    #             if uid is None:
    #                 return {'message': f'User ID is missing'}, 400
    #             password = body.get('password')
                
    #             ''' Find user '''
    #             user = User.query.filter_by(_uid=uid).first()
    #             if user is None or not user.is_password(password):
    #                 return {'message': f"Invalid user id or password"}, 400
    #             if user:
    #                 try:
    #                     token = jwt.encode(
    #                         {"_uid": user._uid},
    #                         current_app.config["SECRET_KEY"],
    #                         algorithm="HS256"
    #                     )
    #                     resp = Response("Authentication for %s successful" % (user._uid))
    #                     resp.set_cookie("jwt", token,
    #                             max_age=3600,
    #                             secure=True,
    #                             httponly=True,
    #                             path='/',
    #                             samesite='None'  # This is the key part for cross-site requests

    #                             # domain="frontend.com"
    #                             )
    #                     return resp
    #                 except Exception as e:
    #                     return {
    #                         "error": "Something went wrong",
    #                         "message": str(e)
    #                     }, 500
    #             return {
    #                 "message": "Error fetching auth token!",
    #                 "data": None,
    #                 "error": "Unauthorized"
    #             }, 404
    #         except Exception as e:
    #             return {
    #                     "message": "Something went wrong!",
    #                     "error": str(e),
    #                     "data": None
    #             }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    # api.add_resource(_Security, '/authenticate')
    