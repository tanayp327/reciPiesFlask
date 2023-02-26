import json
import os
from flask import Blueprint, request
from flask_restful import Api, Resource

favorites_api = Blueprint('favorites_api', __name__, url_prefix='/api/favorites')
api = Api(favorites_api)

# Define a new resource for recipe data
class RecipeData(Resource):
    # Handle POST requests to add a recipe to the favorites
    def post(self):
        # Get the recipe data from the request body
        data = request.get_json()
        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')

        # Read the favorites data from the favorites.json file
        try:
            with open('favorites.json', 'r') as f:
                favorites = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            favorites = []

        for favorite in favorites:
            if favorite['title'] == title:
                return {"message": "Recipe already exists in favorites."}
            
        # Add the recipe to the favorites
        favorites.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})

        # Write the updated favorites data back to the favorites.json file
        with open('favorites.json', 'w') as f:
            json.dump(favorites, f)

        # Return a success message
        return {"message": "Data saved successfully"}

class GetFavorites(Resource):
    # Handle GET requests to retrieve all favorites
    def get(self):
        # Read the favorites data from the favorites.json file
        try:
            with open('favorites.json', 'r') as f:
                favorites = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            favorites = []

        # Return all favorites
        return favorites

# Add the RecipeData resource with the POST endpoint
api.add_resource(RecipeData, '/favorites')

# Add the GetFavorites resource with the GET endpoint
api.add_resource(GetFavorites, '/favorites/all')
