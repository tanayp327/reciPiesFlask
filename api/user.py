from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate rname
            rname = body.get('rname')
            if rname is None or len(rname) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 200
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            comment = body.get('comment')
            if comment is None or len(comment) < 2:
                return {'message': f'Comment is missing, or is less than 2 characters'}, 220            # validate rname
            rating = body.get('rating')
            if rating is None or len(rating) < 1 or int(rating) > 10:
                return {'message': f'Rating is missing, or is out of range'}, 230

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(rname=rname,
                      comment=comment,
                      rating=rating,
                      uid=uid
                      )
            
           
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {rname}, either a format error or User ID {uid} is duplicate'}, 240

    class _Read(Resource):
        def get(self):
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            id = body.get('id')
            print("inside user.py delete id", id)
            user=User.delete(id)
            if user:
                users = User.query.all()    # read/extract all users from database
                json_ready = [user.read() for user in users]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps               

    class _Update(Resource):
        def put(self):
            print("inside user.py put")
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
            print("inside user.py update id", id)
            user=User.put(self, id,comment,rating,uid)
            # user=User.put(id, self.comment, self.rating, self.uid)
            if user:
                users = User.query.all()    # read/extract all users from database
                json_ready = [user.read() for user in users]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps                                     
              
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/update')
    api.add_resource(_Delete, '/delete')
