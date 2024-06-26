""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
# class Post(db.Model):
#     __tablename__ = 'posts'

#     # Define the Notes schema
#     id = db.Column(db.Integer, primary_key=True)
#     note = db.Column(db.Text, unique=False, nullable=False)
#     image = db.Column(db.String, unique=False)
#     # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
#     CharID = db.Column(db.Integer, db.ForeignKey('CharClasses.id'))

#     # Constructor of a Notes object, initializes of instance variables within object
#     def __init__(self, id, note, image):
#         self.CharID = id
#         self.note = note
#         self.image = image

#     # Returns a string representation of the Notes object, similar to java toString()
#     # returns string
#     def __repr__(self):
#         return "Notes(" + str(self.id) + "," + self.note + "," + str(self.CharID) + ")"

#     # CRUD create, adds a new record to the Notes table
#     # returns the object added or None in case of an error
#     def create(self):
#         try:
#             # creates a Notes object from Notes(db.Model) class, passes initializers
#             db.session.add(self)  # add prepares to persist person object to Notes table
#             db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
#             return self
#         except IntegrityError:
#             db.session.remove()
#             return None

#     # CRUD read, returns dictionary representation of Notes object
#     # returns dictionary
#     def read(self):
#         # encode image
#         path = app.config['UPLOAD_FOLDER']
#         file = os.path.join(path, self.image)
#         file_text = open(file, 'rb')
#         file_read = file_text.read()
#         file_encode = base64.encodebytes(file_read)
        
#         return {
#             "id": self.id,
#             "CharID": self.CharID,
#             "note": self.note,
#             "image": self.image,
#             "base64": str(file_encode)
#         }


# # Define the User class to manage actions in the 'users' table
# # -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# # -- a.) db.Model is like an inner layer of the onion in ORM
# # -- b.) User represents data we want to store, something that is built on db.Model
# # -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class CurrentChar(db.Model):
    __tablename__ = 'CurrentChar'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _classname = db.Column(db.String(255), unique=False, nullable=False)
    _health = db.Column(db.Integer, nullable=False)
    _attack = db.Column(db.Integer, nullable=False)
    _range = db.Column(db.Boolean, default=False, nullable=False)
    _movement = db.Column(db.Boolean, default=False, nullable=False)

    
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # posts = db.relationship("Post", cascade='all, delete', backref='CharClasses', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, classname, health, attack, range, movement):
        self._classname = classname    # variables with self prefix become part of the object, 
        self._health = health
        self._attack = attack
        self._range = range
        self._movement = movement

    # a name getter method, extracts name from object
    @property
    def classname(self):
        return self._classname
    
    # a setter function, allows name to be updated after initial object creation
    @classname.setter
    def classname(self, classname):
        self._classname = classname
    
    # a getter method, extracts email from object
    @property
    def health(self):
        return self._health
    
    # a setter function, allows name to be updated after initial object creation
    @health.setter
    def health(self, health):
        self._health = health
        
    # # check if uid parameter matches user id in object, return boolean
    # def is_uid(self, uid):
    #     return self._uid == uid

    # a getter method, extracts email from object
    @property
    def attack(self):
        return self._attack
    
    # a setter function, allows name to be updated after initial object creation
    @attack.setter
    def attack(self, attack):
        self._attack = attack
    
    # a getter method, extracts email from object
    @property
    def range(self):
        return self._range
    
    # a setter function, allows name to be updated after initial object creation
    @range.setter
    def range(self, range):
        self._range = range

    # a getter method, extracts email from object
    @property
    def movement(self):
        return self._movement
    
    # a setter function, allows name to be updated after initial object creation
    @movement.setter
    def movement(self, movement):
        self._movement = movement
    
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
            "classname": self.classname,
            "health": self.health,
            "attack": self.attack,
            "range": self._range,
            "movement": self.movement,
            # "posts": [post.read() for post in self.posts]
        }
        
    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, classname="", health=None, attack=None, range=None, movement=None):
        """only updates values with length"""
        if len(classname) > 0:
            self.classname = classname
            self.health = health
            self.attack = attack
            self._range = range
            self.movement = movement
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
def initCurrentChars():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = CurrentChar(classname='Knight', health=2, attack=2, range=2, movement=1)

        CurrentCharacter = [u1]

        """Builds sample user/note(s) data"""
        for CurrentCharacter in CurrentCharacter:
            try:
                # '''add a few 1 to 4 notes per user'''
                # for num in range(randrange(1, 4)):
                #     note = "#### " + CharClass.classname + " note " + str(num) + ". \n Generated by test data."
                #     CharClass.posts.append(Post(id=CharClass.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                CurrentCharacter.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {CurrentCharacter.classname}")
            