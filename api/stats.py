import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.statsm import Stats
stats_api = Blueprint('stats_api', __name__,
                   url_prefix='/api/stats')
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(stats_api)
class UserAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            playerName = body.get('playerName')
            if playerName is None or len(playerName) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            goals = body.get('goals')
            number = body.get('number')
            stat = Stats( playerName = playerName, uid=uid, goals=goals, number=number)
            created_stat = stat.create()
            if created_stat:
                return jsonify(created_stat.read())
            return {'message': f'Processed {playerName}, either a format error or User ID {uid} is duplicate'}, 400
            ''' Additional garbage error checking '''
            # set password if provided
            # convert to date type
            ''' #2: Key Code block to add user to database '''
            # create user in database
            playerName = uo.create()
            # success returns json of user
            if playerName:
                return jsonify(playerName.read())
            # failure returns error
            return {'message': f'Processed {playerName}, either a format error or User ID {uid} is duplicate'}, 400
        def get(self):
            sort_by = request.args.get('sort_by', 'goals')
            order = request.args.get('order', 'desc')
            if order == 'desc':
                users = Stats.query.order_by(Stats.goals.desc()).all()
            else:
                users = Stats.query.order_by(Stats.goals.asc()).all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)
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
    #             user = Post.query.filter_by(_uid=uid).first()
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
    # api.add_resource(_Security, '/')