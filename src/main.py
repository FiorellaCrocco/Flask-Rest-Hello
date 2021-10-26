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

@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_favorite():

    current_user = get_jwt_identity()

    user = User.query.filter_by(id=current_user).first()

    user_favorite_character = FavoriteCharacter.query.filter_by(user_id=user.id).all()
    user_favorite_planet = Favorite_Planet.query.filter_by(user_id=user.id).all()

    favoritesCharacters = list(map(lambda x: x.serialize(), user_favorite_character))
    favoritesPlanets = list(map(lambda x: x.serialize(), user_favorite_planet))
    return jsonify(favoritesCharacters+favoritesPlanets), 200
 

 ###########################################################################################

#FALTA FILTRAR MEDIANTE EL TOKEN Y CREAR EL CODE PARA QUE HAGA EL POST DE AGREGAR UN PERSONAJE FAVORITO AL USUARIO CON DICHO TOKEN
@app.route('/favorites/character/<int:character_id>', methods=['POST'])
@jwt_required()
def add_favorite_character(character_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    character = Character.query.get(character_id)
    print(character)
    if character is not None and user is not None:
        fav_character = FavoriteCharacter(user_id=user.id, character_id=character.id)
        db.session.add(fav_character)
        db.session.commit()
    return get_favorite()


###########################################################################################
#CREAR LA FUNCIÓN PARA FILTRAR MEDIANTE EL TOKEN Y CREAR EL CODE PARA QUE HAGA EL POST DE AGREGAR UN PLANETA FAVORITO AL USUARIO CON DICHO TOKEN
###########################################################################################
#CREAR LA FUNCIÓN PARA FILTRAR MEDIANTE EL TOKEN Y CREAR EL CODE PARA QUE HAGA EL DELETE DE QUITAR UN PERSONAJE FAVORITO AL USUARIO CON DICHO TOKEN
###########################################################################################
#CREAR LA FUNCIÓN PARA FILTRAR MEDIANTE EL TOKEN Y CREAR EL CODE PARA QUE HAGA EL DELETE DE QUITAR UN PLANETA FAVORITO AL USUARIO CON DICHO TOKEN
###########################################################################################

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
