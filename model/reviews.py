""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Review class to manage actions in the 'reviews' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Review represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Review(db.Model):
    __tablename__ = 'reviews'  # table name is plural, class name is singular

    # Define the Review schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _rname = db.Column(db.String(255), unique=False, nullable=False)
    _comment = db.Column(db.Text, unique=False, nullable=False)
    _rating = db.Column(db.String, unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)    

    # constructor of a Review object, initializes the instance variables within object (self)
    def __init__(self, rname, comment, rating, uid):
        self._rname = rname    # variables with self prefix become part of the object, 
        self._comment = comment
        self._rating = rating
        self._uid = uid

    # a name getter method, extracts name from object
    @property
    def rname(self):
        return self._rname
    
    # a setter function, allows name to be updated after initial object creation
    @rname.setter
    def rname(self, rname):
        self._rname = rname

    # a comment getter method, extracts comment from object
    @property
    def comment(self):
        return self._comment
    
    # a setter function, allows name to be updated after initial object creation
    @comment.setter
    def comment(self, comment):
        self._comment = comment  

    # a getter method, extracts rating from object
    @property
    def rating(self):
        return self._rating
    
    # a setter function, allows name to be updated after initial object creation
    @rating.setter
    def rating(self, rating):
        self._rating = rating              
    
    # a getter method, extracts uid from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
  
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a reviewer object from Review(db.Model) class, passes initializers
            print("Inside create")
            db.session.add(self)  # add prepares to persist person object to Reviews table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # read converts self to dictionary
    # returns dictionary
    def read(self):
        # entry = db.session.query(Reviews).get(args["id"])
        # print(id,self.rname,self.uid,self.comment,self.rating)
        return {
            "id": self.id,
            "rname": self.rname,
            "comment":self.comment,
            "rating":self.rating,
            "uid": self.uid            
        }

    # CRUD update: updates comment, rating, uid
    # returns self
    def put(self,id,comment,rating,uid):
        """only updates values with length"""
        print("inside reviews.py update") 
        entry = db.session.query(Review).get(id)
        print("sent request to update record", entry)  
        print(id,comment,rating,uid)
        try:
            if entry: 
                # db.session.update(self)
                entry.comment = comment
                entry.rating = rating
                entry.uid = uid
                print("updated record", entry)
                db.session.commit()
                return entry
            else:
                return {"error": "entry not found"}, 404                
        except Exception as e:
            db.session.rollback()
            return {"error": f"server error: {e}"}, 500            

    # CRUD delete: remove self
    # None
    def delete(id):
        # print("inside reviews.py delete", id) 
        try:
            entry = db.session.query(Review).get(id)
            if entry: 
                db.session.delete(entry)
                db.session.commit()
                print("deleted record", entry)                
                return None
            else:
                return {"error": "entry not found"}, 404                
        except Exception as e:
            db.session.rollback()
            return {"error": f"server error: {e}"}, 500

"""Database Creation and Testing """


# Builds working data for testing
def initReviews():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = Review(rname='Recipe1', comment='Recipe1 comment', rating=5, uid='toby' )
        u2 = Review(rname='Recipe2', comment='Recipe2 comment', rating=6, uid='niko')
        u3 = Review(rname='Recipe3', comment='Recipe3 comment', rating=3, uid='lex')
        u4 = Review(rname='Recipe4', comment='Recipe4 comment', rating=8, uid='whit')
        u5 = Review(rname='Recipe5', comment='Recipe5 comment', rating=10, uid='jm1021')

        reviews = [u1, u2, u3, u4, u5]

        """Builds sample review/comment(s) data"""
        for review in reviews:
            try:
                review.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {review.uid}")


