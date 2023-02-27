""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _rname = db.Column(db.String(255), unique=False, nullable=False)
    _comment = db.Column(db.Text, unique=False, nullable=False)
    _rating = db.Column(db.Integer, unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)    

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, rname, comment, rating, uid,):
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

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "rname": self.rname,
            "comment":self.comment,
            "rating":self.rating,
            "uid": self.uid            
        }

    # CRUD update: updates recipe name, uid, review, rating
    # returns self
    def update(self, rname="", comment="", rating="", uid=""):
        """only updates values with length"""
        if len(rname) > 0:
            self.rname = rname
        if len(comment) > 0:
            self.comment = comment
        if len(rating) > 0:
            self.rating = rating    
        if len(uid) > 0:
            self.uid = uid                   
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = User(rname='Recipe1', comment='Recipe1 comment', rating=5, uid='toby' )
        u2 = User(rname='Recipe2', comment='Recipe2 comment', rating=6, uid='niko')
        u3 = User(rname='Recipe3', comment='Recipe3 comment', rating=3, uid='lex')
        u4 = User(rname='Recipe4', comment='Recipe4 comment', rating=8, uid='whit')
        u5 = User(rname='Recipe5', comment='Recipe5 comment', rating=10, uid='jm1021')

        users = [u1, u2, u3, u4, u5]

        """Builds sample user/comment(s) data"""
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            