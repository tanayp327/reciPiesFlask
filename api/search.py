from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import time
from flask import Blueprint, request, jsonify
import json
import requests

search_api = Blueprint('search_api', __name__,
                  url_prefix='/api/search')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(search_api)

def searchItem(item):
  filename = 'searches.json'
  result_list = []
  # JSON data:
  x = {"title": "", "ingredients": "", "instructions": ""}

  # Request
  url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"
  querystring = {"query": item}
  headers = {
      "X-RapidAPI-Key": "cb84e1853amsh36bd127c21f5c41p12163cjsn5ce359cf2f1a",
      "X-RapidAPI-Host": "recipe-by-api-ninjas.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)
    # Read JSON file
  with open(filename) as fp:
    listObj = json.load(fp)
  parse_req = response.json()
  for i in range(len(parse_req)):
      title = parse_req[i]["title"]
      ingredients = parse_req[i]["ingredients"]
      instructions = parse_req[i]["instructions"]
      # JSON data:
      x  =  {
          "title": title,
          "ingredients": ingredients,
          "instructions": instructions
      }
      result_list.append(x)
      with open(filename, 'w') as json_file:
        json.dump(result_list, json_file, 
                        indent=4,  
                        separators=(',',': '))
  return result_list

def recentSearches():
    search_list = []
    f = open('searches.json')
    data = json.load(f)
    for i in data:
      search_list.append(i)
    return(search_list)

def deleteSearches():
  with open("searches.json", "w") as f:
      # Write an empty JSON object to the file
      json.dump([], f)

class itemAPI:
    class _Create_Update(Resource):
        def post(self):
            body = request.get_json()
            return searchItem(body.get("item"))
    class _Read(Resource):
        def get(self):
            return recentSearches()
    class _Delete(Resource):
        def get(self):
            deleteSearches()
            return { "Status" : "Successfully Deleted Recent Searches"}

        
    api.add_resource(_Create_Update, '/')
    api.add_resource(_Read, '/recently')
    api.add_resource(_Delete, '/delete')