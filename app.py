from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os # core Python module

# Init app ===============================================
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)
# =======================================================

# ALL models!

# Product Class/Model ===================================

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    character_class = db.Column(db.String(25))
    race = db.Column(db.String(25))
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)

    def __init__(self, name, character_class, race, strength, dexterity, constitution, intelligence, wisdom, charisma): # similar to this in javascript!!
        self.name = name
        self.character_class = character_class
        self.race = race
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

# =======================================================

# Schema ================================================
class CharacterSchema(ma.Schema):
    class Meta: # the fields that we'll show
        fields = ('id', 'name', 'character_class', 'race', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma')

## Init schema
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True) # either dealing with a single product or multiple products

# Routes ================================================
# Create a new character
@app.route('/create_character', methods=['POST'])
def create_character():
    name = request.json['name']
    character_class = request.json['character_class']
    race = request.json['race']
    strength = request.json['strength']
    dexterity = request.json['dexterity']
    constitution = request.json['constitution']
    intelligence = request.json['intelligence']
    wisdom = request.json['wisdom']
    charisma = request.json['charisma']

    new_character = Character(name, character_class, race, strength, dexterity, constitution, intelligence, wisdom, charisma)

    db.session.add(new_character)
    db.session.commit()

    return character_schema.jsonify(new_character)
    

# Get all characters
@app.route('/all_characters', methods=['GET'])
def get_characters():
    all_characters = Character.query.all()
    result = characters_schema.dump(all_characters)
    return jsonify(result)


# Get one character
@app.route('/get_character/<int:id>', methods=['GET'])
def get_character(id:int):
    character = Character.query.get(id)
    return character_schema.jsonify(character)


# Create a new character
@app.route('/update_character/<id>', methods=['PUT'])
def update_character(id):
    character = Character.query.get(id)
    character.name = request.json['name']
    character.character_class = request.json['character_class']
    character.race = request.json['race']
    character.strength = request.json['strength']
    character.dexterity = request.json['dexterity']
    character.constitution = request.json['constitution']
    character.intelligence = request.json['intelligence']
    character.wisdom = request.json['wisdom']
    character.charisma = request.json['charisma']
    # no need to add
    db.session.commit()

    return character_schema.jsonify(character)


# Deletes a characters
@app.route('/delete_character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    return character_schema.jsonify(character)

# ==============================================================

# run server
if __name__ == '__main__':
    app.run(debug=True)