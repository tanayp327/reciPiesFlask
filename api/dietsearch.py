import json
import hashlib
from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import time
from flask import Blueprint, request, jsonify
import requests

url = "https://edamam-recipe-search.p.rapidapi.com/search"

querystring = {"q":"chicken"}

headers = {
	"X-RapidAPI-Key": "cb84e1853amsh36bd127c21f5c41p12163cjsn5ce359cf2f1a",
	"X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)