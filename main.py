import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from model.jokes import initJokes
from model.reviews import initReviews

# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.review import review_api # Blueprint import api definition
from api.search import search_api 
from api.favorites import favorites_api
from api.dietsearch import restrictions_api

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# register URIs
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(review_api) # register api routes
app.register_blueprint(search_api)
app.register_blueprint(restrictions_api)
app.register_blueprint(favorites_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.before_first_request
def activate_job():
    initJokes()
    initReviews()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    CORS(app)
    app.run(debug=True, host="0.0.0.0", port="8086")
