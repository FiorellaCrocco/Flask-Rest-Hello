"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():

    user_query = User.query.all()

    all_user = list(map(lambda x: x.serialize(), user_query))

    return jsonify(all_user), 200

@app.route('/character', methods=['GET'])
def get_character():

    character_query = Character.query.all()

    all_character = list(map(lambda x: x.serialize(), character_query))

    return jsonify(all_character), 200

@app.route('/planet', methods=['GET'])
def get_planet():

    planet_query = Planet.query.all()

    all_planet = list(map(lambda x: x.serialize(), planet_query))

    return jsonify(all_planet), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_character_id(id):

    character_query = Character.query.get(id)

    character = character_query.serialize()

    return jsonify(character), 200

@app.route('/<email>/favorites', methods=['GET'])
def get_favorite(email):

    user = User.query.filter_by(email=email).first()

    user_favorite_character = FavoriteCharacter.query.filter_by(user_id=user.id).all()

    favorites = list(map(lambda x: x.serialize(), user_favorite_character))

    return jsonify(favorites), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
