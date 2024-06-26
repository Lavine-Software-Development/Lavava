from email.policy import default
import jwt
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(80), nullable=False, default="haha") # todo: remove default, fix frontend
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    elo = db.Column(db.Integer, default=1100)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), default=None)

# Deck table
class Deck(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ability = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    secondary_id = db.Column(db.Integer, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('secondary_id', 'ability', name='_deck_secondary_id_ability_uc'),
    )
# Game table
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_ids = db.Column(db.JSON, nullable=False)  # Example: [1, 2, 3, 4]
    user_ranks = db.Column(db.JSON, nullable=False)  # Example: {"1": "1st", "2": "2nd", "3": "3rd", "4": "4th"}

with app.app_context():
# def create_tables():
    # Deck.__table__.drop(db.engine)
    db.create_all()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Assuming bearer token is used
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    # todo: remove default

    if username.lower() == 'default':
        # Create a token
        token = jwt.encode({
            'user': username,
            # 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=72)  # Token expires in 24 hours?
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)  # Token expires in 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200

    if user and check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


    if username.lower() == 'default':
        # Create a token
        token = jwt.encode({
            'user': username,
            # 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=72)  # Token expires in 24 hours?
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)  # Token expires in 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    display_name = data.get('display_name')
    email = data.get('email')  # Email is received but not used in logic for simplicity
    password = data.get('password')  # Password is received but not used in logic
    
    # if username.lower() == 'default':
    #     return jsonify({"success": True, "message": "Registration successful"}), 200
    # else:
    #     return jsonify({"success": False, "message": "Registration failed, username must be 'default'"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "Username already exists"}), 400
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, display_name=display_name, email=email, password=hashed_password) # type: ignore
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "Registration successful"}), 200
    
@app.route('/user_abilities', methods=['GET'])
@token_required
def get_home(current_user):

    user = User.query.filter_by(username=current_user).first()
    if user and user.deck_id:
        deck = Deck.query.filter_by(id=user.deck_id).first()
        return jsonify({
            "abilities": user_decks(current_user)
        })
    else:
        return jsonify({"error": "User not found or no deck assigned"}), 404
    
    if current_user == "default":
        return jsonify({
            "abilities": user_decks(current_user),
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if current_user == "default":
        return jsonify({
            "userName": "Default-User",
            "displayName": "John Doe",
            "email": "john.doe@example.com",
            "abilities": user_decks(current_user),
            "elo": 1138,
            "past_games": ["1st", "4th", "2nd"]
        })
    else:
        return jsonify({"error": "User not found"}), 404
    

def user_decks(current_user):
    if current_user == "default":
        return [{"name": "Capital", "count": 1}, {"name": "Cannon", "count": 1}, {"name": "Rage", "count": 2}, {"name": "Poison", "count": 1}]
    else:
        user = User.query.filter_by(username=current_user).first()
        decks = Deck.query.filter_by(secondary_id=user.id).all()
        abilites = []
        for deck in decks: 
            abilites.append({"name": deck.ability, "count": deck.count})
        return abilites
    
@app.route('/save_deck', methods=['POST'])
@token_required
def save_deck(current_user):
    data = request.json
    abilities = data.get('abilities')
    user = User.query.filter_by(username=current_user).first()

    if not abilities:
        delete_rows_with_secondary_id(user.id)
        return jsonify({"success": False, "message": "Missing abilities"}), 400

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # Ensure items count is valid
    # assert len(abilities) < 4 and all(item['count'] > 0 for item in abilities)

    if user.deck_id is None:
        # Find the maximum deck_id and increment it
        max_deck_id = db.session.query(db.func.max(Deck.id)).scalar()
        new_deck_id = (max_deck_id or 0) + 1
        user.deck_id = new_deck_id
        db.session.commit()

    # Delete old deck entries for the user
    Deck.query.filter_by(id=user.deck_id).delete()
    db.session.commit()

    # Save new deck entries
    # deck_id=user.deck_id, 
    for item in abilities:
        new_deck_entry = Deck(secondary_id=user.deck_id, ability=item['name'], count=item['count'])
        add_or_replace_deck(secondary_id=user.deck_id, ability=item['name'], count=item['count'])
    
    db.session.commit()

    # # Convert abilities list to a dictionary
    # items = {item['name']: item['count'] for item in abilities}
    # new_deck = Deck(items=items, count=count)
    # db.session.add(new_deck)
    # db.session.commit()

    # Update user's deck_id
    # user.deck_id = new_deck.id
    # db.session.commit()

    return jsonify({"success": True, "message": "Deck saved successfully"}), 200
    
@app.route('/abilities', methods=['GET'])
def get_abilities():
    abilities = [
        {"name": "Freeze", "cost": 1},
        {"name": "Spawn", "cost": 1},
        {"name": "Zombie", "cost": 1},
        {"name": "Burn", "cost": 1},
        {"name": "Poison", "cost": 2},
        {"name": "Rage", "cost": 2},
        {"name": "D-Bridge", "cost": 2},
        {"name": "Bridge", "cost": 2},
        {"name": "Capital", "cost": 3},
        {"name": "Nuke", "cost": 3},
        {"name": "Cannon", "cost": 3},
        {"name": "Pump", "cost": 3},
    ]
    return jsonify({"abilities": abilities, "salary": 15})
def add_or_replace_deck(secondary_id, ability, count):
    try:
        new_deck_entry = Deck(
            secondary_id=secondary_id,
            ability=ability,
            count=count
        )
        db.session.add(new_deck_entry)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing_deck_entry = db.session.query(Deck).filter_by(
            secondary_id=secondary_id,
            ability=ability
        ).one()
        existing_deck_entry.count = count
        db.session.commit()
def delete_rows_with_secondary_id(secondary_id):
    try:
        db.session.query(Deck).filter_by(secondary_id=secondary_id).delete()
        db.session.commit()
        print(f"All rows with secondary_id = {secondary_id} have been deleted.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5001)
