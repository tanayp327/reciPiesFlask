from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import json

getusers_api = Blueprint('getusers_api', __name__, url_prefix='/api/getusers')
api = Api(getusers_api)


class usersAPI:
	class _Read(Resource):
		def get(self):
			counter = 0
			with open('users.json') as menu_file:
				items = json.load(menu_file)
				return(len(items))
	api.add_resource(_Read, '/')
