import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from models import db, User, Character, Planet, FavoriteCharacter, Favorite_Planet
#from models import Person

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "aprendiendo-token"  # Change this!
jwt = JWTManager(app)

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def Login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()
    if User is None:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })


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

@app.route('/character/<int:id>', methods=['GET'])
def get_character_id(id):

    character_query = Character.query.get(id)

    character = character_query.serialize()

    return jsonify(character), 200

@app.route('/planet', methods=['GET'])
def get_planet():

    planet_query = Planet.query.all()

    all_planet = list(map(lambda x: x.serialize(), planet_query))

    return jsonify(all_planet), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_id(id):

    planet_query = Planet.query.get(id)

    planet = planet_query.serialize()

    return jsonify(planet), 200

#HACERLA PRIVADA
@app.route('/<email>/favorites', methods=['GET'])
def get_favorite(email):

    user = User.query.filter_by(email=email).first()

    user_favorite_character = FavoriteCharacter.query.filter_by(user_id=user.id).all()

    favorites = list(map(lambda x: x.serialize(), user_favorite_character))

    return jsonify(favorites), 200
 
@app.route('/favorites/character/<int:character_id>', methods=['POST'])
def add_favorite(character_id):
    #USAR TOKEN / HACERLA PRIVADA
    return jsonify(favorites), 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
