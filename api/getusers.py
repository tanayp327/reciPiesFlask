from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import json

getusers_api = Blueprint('getusers_api', __name__, url_prefix='/api/getusers')
api = Api(getusers_api)

def getUsers():
	counter = 0
	with open('users.json') as menu_file:
		items = json.load(menu_file)
		return(len(items))
	if counter == 0:
		return {"No Users"}

class usersAPI:
	class _Read(Resource):
		def get(self):
			return(getUsers())
	api.add_resource(_Read, '/')
