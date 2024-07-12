import jwt
import datetime
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from functools import wraps
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'


if config.DB_CONNECTED:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        display_name = db.Column(db.String(80), nullable=False, default="Not Yet Specified")
        password = db.Column(db.String(200), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        elo = db.Column(db.Integer, default=1100)
        email_confirm = db.Column(db.Boolean, nullable=False, default=False)

        def __init__(self, username, password, email):
            self.username = username
            self.password = password
            self.email = email

    class Deck(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

        def __init__(self, name, user_id):
            self.name = name
            self.user_id = user_id

    class DeckCard(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
        ability = db.Column(db.String(50), nullable=False)
        count = db.Column(db.Integer, nullable=False)

        def __init__(self, deck_id, ability, count):
            self.deck_id = deck_id
            self.ability = ability
            self.count = count

    class Game(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        game_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
        user_ids = db.Column(db.JSON, nullable=False)
        user_ranks = db.Column(db.JSON, nullable=False)


    with app.app_context():
    # def create_tables():
        # Deck.__table__.drop(db.engine)
        db.create_all()

# for the email register
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lavavaacc@gmail.com'
app.config['MAIL_PASSWORD'] = 'enwueidxiwivjvxn'  # Use the app password you generated
mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY']) # serializer

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Assuming bearer token is used
            except IndexError:
                return jsonify({'message': 'Invalid Authorization header format!'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login_identifier = data.get('username')  # This could be either username or email
    password = data.get('password')

    if not login_identifier or not password:
        return jsonify({"message": "Missing login identifier or password"}), 400

    if not config.DB_CONNECTED:
        if login_identifier.lower() in ('default', 'other'):
            token = jwt.encode({
                'user': login_identifier,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)  # Token expires in 24 hours
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({"token": token}), 200
    
        return jsonify({"message": "Invalid credentials"}), 401

    user = User.query.filter(
        or_(User.username == login_identifier, User.email == login_identifier)).first()

    if not user:
        return jsonify({"message": "User not found"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    if not user.email_confirm:
        return jsonify({"message": "Email not confirmed"}), 401

    token = jwt.encode({
        'user_id': user.id,
        'user': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"token": token}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')  # Email is received and will be used to send welcome email
    password = data.get('password') # password received and used to check requirements before sending email

    if config.DB_CONNECTED:
        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "Username already exists"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Account with this email already exists"}), 400
    elif username.lower() not in ('default', 'other'):
        return jsonify({"success": False, "message": "Registration failed, username must be 'default or other'"}), 400
        
    if password_requirements(password) is not True:
         return password_requirements(password)
    token = s.dumps(email, salt='email-confirm')
    link = url_for('confirm_email', token=token, _external=True)
    send_confirmation_email(email, link)  # Send confirm email
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    if config.DB_CONNECTED:
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    return jsonify({"success": True, "message": "Please follow the confirmation email sent to: {} (check spam mail)".format(email)}), 200


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600) # token expires after 1 hour
    except SignatureExpired:
        return '<h1>Email confirmation link expired!</h1>' # token expired
    except:
        return '<h1>Error!</h1>' # other error like incorrect token
    if config.DB_CONNECTED:
        user = User.query.filter_by(email=email).first()
        if not user:
            return '<h1>Error!</h1>'
        user.email_confirm = True
        db.session.commit()
    return '<h1>Email Confirmed!</h1><p>Proceed to login page to login.</p>' 

#  sending email for registration
def send_confirmation_email(user_email, link):
    msg = Message("Email Confirmation!",
                  sender='lavavaacc@gmail.com',
                  recipients=[user_email])
    msg.body = 'Follow the link to confirm your account: {}'.format(link)
    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return "Error sending email."


@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    username = data.get('username') # email or username
    password = data.get('password') 
    repeatPassword = data.get('repeatPassword')

    if password != repeatPassword:
        return jsonify({"success": False, "message": "Password and repeat password must match"}), 400
    if password_requirements(password) is not True:
         return password_requirements(password)
    if config.DB_CONNECTED:
        if User.query.filter_by(username=username).first(): # user found with username
            user = User.query.filter_by(username=username).first()
            username = user.email # changing variable to email of account with entered username
        if User.query.filter_by(email=username).first(): # checking if there is an account with the entered email
            passwordToken = password + " " + username
            token = s.dumps(passwordToken, salt='reset-password')
            link = url_for('confirm_password_reset', token=token, _external=True)
            send_reset_email(username, link)  # Send confirm email
            return jsonify({"success": True, "message": "Password reset email sent! Click the link sent to confirm password reset. Click below to login"}), 200
        else:
            return jsonify({"success": False, "message": "No account with this username or email exists."}), 404
    else:
        return jsonify({"success": False, "message": "Database connection error"}), 500


def send_reset_email(user_email, link):
    msg = Message("Reset Password - Ignore if not requested!",
                  sender='lavavaacc@gmail.com',
                  recipients=[user_email])
    msg.body = 'IGNORE AND DO NOT CLICK THE LINK BELOW if you did not request to change your password.\n\nIf you did request a password reset follow the link to confirm your password reset: {} \nThis link will expire in 5 minutes.'.format(link)
    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return "Error sending email."
    

@app.route('/confirm_password_reset/<token>')
def confirm_password_reset(token):
    try:
        passwordToken = s.loads(token, salt='reset-password', max_age=300) # token expires after 5 minutes
    except SignatureExpired:
        return '<h1>Reset password link expired!</h1>' # token expired
    except:
        return '<h1>Error!</h1>' # other error like incorrect token
    password_and_email = passwordToken.split(" ")
    hashed_password = generate_password_hash(password_and_email[0], method='pbkdf2:sha256')
    if config.DB_CONNECTED:
        user = User.query.filter_by(email=password_and_email[1]).first()
        if not user:
            return '<h1>Error!</h1>'
        user.password = hashed_password
        db.session.commit()
    return '<h1>Password Reset Successful!</h1>' 


@app.route('/change_password', methods=['POST'])
@token_required
def change_password(current_user):
    data = request.json
    password = data.get('password') 
    repeatPassword = data.get('repeatPassword')

    if password != repeatPassword:
        return jsonify({"success": False, "message": "Password and repeat password must match"}), 400
    if password_requirements(password) is not True:
         return password_requirements(password)
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            user.password = generate_password_hash(password, method='pbkdf2:sha256')
            db.session.commit()
            return jsonify({"success": True, "message": "Password change successful!"}), 200
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    else:
        return jsonify({"success": False, "message": "Database connection error"}), 500
        

def password_requirements(password): # checks for password requirements returns true if passed requirements
    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400
    if not any(char.islower() for char in password):
        return jsonify({"success": False, "message": "Password must have at least one lowercase letter"}), 400
    if not any(char.isupper() for char in password):
        return jsonify({"success": False, "message": "Password must have at least one uppercase letter"}), 400
    if ' ' in password:
        return jsonify({"success": False, "message": "Password cannot contain spaces"}), 400
    else:
        return True


@app.route('/user_abilities', methods=['GET'])
@token_required
def get_home(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            return jsonify({
                "abilities": user_decks(current_user)
            })
        else:
            return jsonify({"error": "User not found or no deck assigned"}), 404
    
    elif current_user in {"default", "other"}:
        return jsonify({
            "abilities": user_decks(current_user),
        })
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            games = Game.query.filter(Game.user_ids.contains(str(user.id))).order_by(Game.game_date.desc()).limit(3).all()
            past_games = [game.user_ranks.get(str(user.id), "N/A") for game in games]
            return jsonify({
                "userName": user.username,
                "displayName": user.display_name,
                "email": user.email,
                "abilities": user_decks(current_user),
                "elo": user.elo,
                "past_games": past_games
            })
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({
            "userName": "Default-User",
            "displayName": "John Doe",
            "email": "john.doe@example.com",
            "abilities": user_decks(current_user),
            "elo": 1138,
            "past_games": ["1st", "4th", "2nd"]
        })
    

def user_decks(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            deck = Deck.query.filter_by(user_id=user.id).first()
            if deck:
                cards = DeckCard.query.filter_by(deck_id=deck.id).all()
                return [{"name": card.ability, "count": card.count} for card in cards]
        return []  # Return empty list if no user or no deck
    else:
        return [{"name": "Capital", "count": 1}, {"name": "Cannon", "count": 1}, {"name": "Rage", "count": 2}, {"name": "Poison", "count": 1}]
    

@app.route('/save_deck', methods=['POST'])
@token_required
def save_deck(current_user):
    if not config.DB_CONNECTED:
        return jsonify({"success": False, "message": "Database not connected"}), 500

    data = request.json
    abilities = data.get('abilities')

    if not abilities:
        return jsonify({"success": False, "message": "Missing abilities"}), 400

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    try:
        # Get or create the user's deck
        deck = Deck.query.filter_by(user_id=user.id).first()
        if not deck:
            deck = Deck(user_id=user.id, name="Default Deck")
            db.session.add(deck)
            db.session.flush()  # This assigns an ID to the deck if it's new

        # Get current deck cards
        current_cards = {card.ability: card for card in DeckCard.query.filter_by(deck_id=deck.id)}

        # Update deck
        for ability in abilities:
            if ability['name'] in current_cards:
                # Update existing card
                current_cards[ability['name']].count = ability['count']
                current_cards.pop(ability['name'])
            else:
                # Add new card
                new_card = DeckCard(deck_id=deck.id, ability=ability['name'], count=ability['count'])
                db.session.add(new_card)

        # Remove cards not in the new deck
        for card in current_cards.values():
            db.session.delete(card)

        db.session.commit()
        return jsonify({"success": True, "message": "Deck saved successfully"}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Error saving deck"}), 500

def update_elos(new_elos, usernames):
    if config.DB_CONNECTED:
        for username, new_elo in zip(usernames, new_elos):
            user = User.query.filter_by(username=username).first()
            if user:
                user.elo = new_elo
        db.session.commit()
    else:
        print("Database not connected. Elo updates not saved.")

def calculate_elos(elos, k_factor=32):
    n = len(elos)
    new_elos = elos.copy()
    
    for i in range(n):
        for j in range(i+1, n):
            expected_i = 1 / (1 + 10**((elos[j] - elos[i]) / 400))
            expected_j = 1 - expected_i
            
            score_i = 1  # Player i won against player j
            score_j = 0  # Player j lost against player i
            
            new_elos[i] += k_factor * (score_i - expected_i)
            new_elos[j] += k_factor * (score_j - expected_j)
    
    return [round(elo) for elo in new_elos]

def token_to_username(token: str):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user']
    except jwt.ExpiredSignatureError:
        return 'Expired token'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def username_to_elo(name: str):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=name).first()
        return user.elo if user else 1100  # Default ELO if user not found
    else:
        dummy = {"other": 1200, "default": 1300}
        return dummy.get(name, 1100)  # Def
    
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

@app.route('/elo', methods=['POST'])
def update_elo():
    # important that order is maintained throughout the process, as that preserves ranking in game
    # hence why lists are used
    # first two method calls are placeholders for actual db queries
    ordered_tokens = request.json.get("ordered_players")

    usernames = [token_to_username(token) for token in ordered_tokens]
    old_elos = [username_to_elo(user) for user in usernames]
    new_elos = calculate_elos(old_elos)

    update_elos(new_elos, usernames)

    elo_tuples = {ordered_tokens[i]: list(zip(old_elos, new_elos))[i] for i in range(len(ordered_tokens))}
    return jsonify({"new_elos": elo_tuples})


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    if config.DB_CONNECTED:
        # Query the database for all confirmed users, ordered by elo descending
        confirmed_users = User.query.filter_by(email_confirm=True).order_by(desc(User.elo)).all()
        leaderboard = [
            {"userName": user.username, "elo": user.elo} 
            for user in confirmed_users
        ]
        return jsonify({"leaderboard": leaderboard})
    
    return jsonify({
        "leaderboard": [
            {"userName": "Default-User", "elo": 1138},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "Alice", "elo": 1500},
            {"userName": "Bob", "elo": 1400},
            {"userName": "Charlie", "elo": 1300},
            {"userName": "David", "elo": 1200}
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
