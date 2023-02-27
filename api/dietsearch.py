from contextlib import nullcontext
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource 
import time
import json
import requests

# Blueprints enable python code to be organized in multiple files and directories https://flask.palletsprojects.com/en/2.2.x/blueprints/
restrictions_api = Blueprint('restrictions_api', __name__,
                   url_prefix='/api/dietsearch')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(restrictions_api)

# new code
def searchItem(item):
    output = []
    app_id = 'be8c6268'
    app_key = '1da5fbf54060504cc2506d8c9fff673a'
    items = "&health=".join(item)
    url = f'https://api.edamam.com/api/recipes/v2?app_id={app_id}&app_key={app_key}&type=public&{items}'

    print("DBG: Making a request: " + url)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for hit in data['hits']:
            print("Processing hit")
            recipe = hit['recipe']
            label = recipe['label']
            calories = recipe['calories']
            totalTime = recipe['totalTime']
            ingredients = recipe['ingredients']
            x = {
                    "label": label,
                    "calories": calories,
                    "totalTime": str(totalTime) + " minutes",
                    "ingredients": [qq['text'] for qq in ingredients]
            }

            # for ingredient in ingredients:
            #     print(f'\t{ingredient["text"]}')
            output.append(x)
        return(output)
    else:
        print(f'Request failed with status code {response.status_code}')


class itemAPI:
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            return searchItem(body.get("item"))

    api.add_resource(_Create, '/')