from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import time

# Blueprints enable python code to be organized in multiple files and directories https://flask.palletsprojects.com/en/2.2.x/blueprints/
recipe_api = Blueprint('recipe_api', __name__,
                   url_prefix='/api/recipe')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(recipe_api)

"""Time Keeper
Returns:
    Boolean: is it time to update?
"""
def updateTime():
    global last_run  # the last_run global is preserved between calls to function
    try: last_run
    except: last_run = None
    
    # initialize last_run data
    if last_run is None:
        last_run = time.time()
        return True
    
    # calculate time since last update
    elapsed = time.time() - last_run
    if elapsed > 86400:  # update every 24 hours
        last_run = time.time()
        return True
    
    return False

"""API Handler
Returns:
    String: API response
"""   
def getRecipeAPI():
    global recipe_data  # the recipe_data global is preserved between calls to function
    try: recipe_data
    except: recipe_data = None

    """
    Preserve Service usage / speed time with a Reasonable refresh delay
    """
    if updateTime(): # request recipe data
        """
        RapidAPI is the world's largest API Marketplace. 
        Developers use Rapid API to discover and connect to thousands of APIs. 
        """
        url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
        querystring = {"ingr":"apple"}
        headers = {
            "X-RapidAPI-Key": "26d9a3c8fbmshd1c8fc32ca8acc3p190a69jsn54f737b8e33b",
            "X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        recipe_data = response
    else:  # Request recipe Data
        response = recipe_data

    return response


"""API with Filter
Returns:
    String: Filter of API response
"""   
def getCategory(filter):
    # Request recipe Data
    response = getRecipeAPI()
    
    # all recipes are under 'hints'
    all_rep = response.json().get('hints')

    # two categories : 'Generic meals' / 'Packaged foods'
    rep_list = []  # store all recipes
    for rep in all_rep:
        rep_temp = rep['food']
        if rep_temp['category'].lower() == filter.lower():
            rep_list.append(rep)
            
    return rep_list


"""Defines API Resources 
  URLs are defined with api.add_resource
"""   
class RecipeAPI:
    """API Method to GET all recipe Data"""
    class _Read(Resource):
        def get(self):
            return getRecipeAPI().json()
        
    """API Method to GET recipe Data for a Specific Category"""
    class _ReadCategory(Resource):
        def get(self, filter):
            return jsonify(getCategory(filter))
    
    # resource is called an endpoint: base usr + prefix + endpoint
    api.add_resource(_Read, '/')
    api.add_resource(_ReadCategory, '/<string:filter>')