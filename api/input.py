import json
import hashlib
from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import time
from flask import Blueprint, request, jsonify
import json
import requests

input_api = Blueprint('input_api', __name__,
                   url_prefix='/api/input')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(input_api)

# Checks if the 
def validation(username, password):
  password = hashlib.sha256(str(password))

# Checks if the user is valid, and then adds items to a list (database) which will be appended to the site
def takeInput(title, ingredients, instructions):
    # adds the input data into a table
    item = {
      "title": title, 
      "ingredients": ingredients, 
      "instructions": instructions
    }
    inputList = []
    with open("userInput.json", "a") as jsonfile:
      inputList.append(item)
      json.dump(item, jsonfile)
    return("Successfully added")

class inputAPI:
    class _Read(Resource):
        def post(self):
            body = request.get_json()
            title =body.get("title")
            ingredients = body.get("ingredients")
            instructions = body.get("instructions")
            username = body.get("username")
            password = body.get("password")
            if validation(username, password):
              return(takeInput(title, ingredients, instructions))
            else:
              return("Inaccurate Validation")
              

    api.add_resource(_Read, '/')
