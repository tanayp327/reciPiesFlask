from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import time
from flask import Blueprint, request, jsonify
import json
import requests


signup_api = Blueprint('signup_api', __name__, url_prefix='/api/signup')
api = Api(signup_api)

def getUsers():
	counter = 0
	with open('users.json') as menu_file:
		items = json.load(menu_file)
		return(len(items))


class signupAPI:
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            username = jsonify(body.get('username'))
            return(username)

    api.add_resource(_Create, '/')
