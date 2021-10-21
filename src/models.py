from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_character = db.relationship('Favorite_Character', backref='user')
    favorite_planet = db.relationship('Favorite_Planet', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)
    mass = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.username

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "gender":self.gender,
            "hair_color":self.hair_color,
            "eye_color":self.eye_color,
            "height":self.height,
            "mass":self.mass,
            "skin_color":self.skin_color,
            "birth_year":self.birth_year
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    rotation_period = db.Column(db.String(80), unique=False, nullable=False)
    orbital_period = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.username

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "diameter":self.diameter,
            "climate":self.climate,
            "gravity":self.gravity,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
            "population":self.population
        }

class Favorite_Character(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    
    def __repr__(self):
        return '<Favorite_Character %r>' % self.username

    def serialize(self):
        return {
            "user_id":self.user_id,
            "character_id":self.character_id
        }

class Favorite_Planet(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return '<Favorite_Planet %r>' % self.username

    def serialize(self):
        return {
            "user_id":self.user_id,
            "planet_id":self.character_id
        }