from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    favoriteses = db.relationship('Favorites', backref="owner")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Peoples(db.Model):
    __tablename__='people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref="character")

    def __repr__(self):
        return '<Peoples %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name_people": self.name,
            "description": self.description
        }

class Favorites(db.Model): 
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, ForeignKey("planets.id"), nullable=True)
    people_id = db.Column(db.Integer, ForeignKey("people.id"), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def __init__(self, name, user_id, planet_id, people_id):
        self.name = name
        self.user_id = user_id
        self.planet_id = planet_id
        self.people_id = people_id
        
    @classmethod
    def new_registro_favorites(cls, name, user_id, planet_id, people_id):
        new_registro_favorites = cls(name, user_id, planet_id, people_id)
       
        db.session.add(new_registro_favorites)
        try:
            db.session.commit()
            return new_registro_favorites
        except Exception as error:
            print(error)
            return None

    def update(self, name):
        self.name = name
        try:
            db.session.commit()
            return self
        except Exception as error:
            print(error)
            return False

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def serialize(self):
        return {
            "id": self.id,
            "name_favorites": self.name,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
        }

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref="planets")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name_planets": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }