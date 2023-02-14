import json
import hashlib
from contextlib import nullcontext
from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource
import time
import requests

app = Flask(__name__)
api = Api(app)

class RecipeData(Resource):
    def post(self, user_id):
        data = request.get_json()
        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')

        with open('users.json', 'r') as f:
            users = json.loads(f.read())

        for user in users:
            if user['UserID'] == user_id:
                user['Favorites'].append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
                
                with open('users.json', 'w') as f:
                    f.write(json.dumps(users))

                return {"message": "Data saved successfully"}

        return {"error": "User not found"}

    def get(self, user_id):
        with open('users.json', 'r') as f:
            users = json.loads(f.read())
            for user in users:
                if user['UserID'] == user_id:
                    return user['Favorites']
        
        return {"error": "User not found"}

api.add_resource(RecipeData, '/user/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
