from contextlib import nullcontext
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource 
import time
import json
import requests

# Blueprints enable python code to be organized in multiple files and directories https://flask.palletsprojects.com/en/2.2.x/blueprints/
recipe_api = Blueprint('recipe_api', __name__,
                   url_prefix='/api/recipe')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(recipe_api)


# new code

app_id = 'be8c6268'
app_key = '1da5fbf54060504cc2506d8c9fff673a'

url = f'https://api.edamam.com/api/recipes/v2?app_id={app_id}&app_key={app_key}&type=public&q=lentils'

response = requests.get(url)

if response.status_code == 200:
    print(response.json())
else:
    print(f'Request failed with status code {response.status_code}')