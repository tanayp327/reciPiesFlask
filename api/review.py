from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.reviews import Review

review_api = Blueprint('review_api', __name__,
                   url_prefix='/api/reviews')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(review_api)

class ReviewAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate rname
            rname = body.get('rname')
            if rname is None or len(rname) < 2:
                return {'message': 'Name is missing, or is less than 2 characters'}, 200
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': 'Review ID is missing, or is less than 2 characters'}, 210
            comment = body.get('comment')
            if comment is None or len(comment) < 2:
                return {'message': 'Comment is missing, or is less than 2 characters'}, 220            # validate rname
            rating = body.get('rating')
            if rating.isnumeric() == "false" or int(rating) > 10:
                return {'message': 'Rating is missing/alpha, or is out of range'}, 230

            ''' #1: Key code block, setup REVIEW OBJECT '''
            uo = Review(rname=rname,
                      comment=comment,
                      rating=rating,
                      uid=uid
                      )
            
           
            ''' #2: Key Code block to add review to database '''
            # create review in database
            review = uo.create()
            # success returns json of review
            if review:
                return jsonify(review.read())
            # failure returns error
            return {'message': f'Processed {rname}, either a format error or Review ID {uid} is duplicate'}, 240

    class _Read(Resource):
        def get(self):
            reviews = Review.query.all()    # read/extract all reviews from database
            json_ready = [review.read() for review in reviews]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            id = body.get('id')
            print("inside review.py delete id", id)
            review=Review.delete(id)
            if review:
                reviews = Review.query.all()    # read/extract all reviews from database
                json_ready = [review.read() for review in reviews]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps               

    class _Update(Resource):
        def put(self):
            print("inside review.py put")
            body = request.get_json()
            id = body.get('id')
            comment = body.get('comment')
            rating = body.get('rating')
            uid = body.get('uid')
            # self.id = id
            # if len(comment) > 0:
            #     self.comment = comment
            # if rating >= 10:
            #     self.rating = rating    
            # if len(uid) > 0:
            #     self.uid = uid 
            print("inside review.py update id", id)
            review=Review.put(self, id,comment,rating,uid)
            # review=Review.put(id, self.comment, self.rating, self.uid)
            if review:
                reviews = Review.query.all()    # read/extract all reviews from database
                json_ready = [review.read() for review in reviews]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
              
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/update')
    api.add_resource(_Delete, '/delete')
