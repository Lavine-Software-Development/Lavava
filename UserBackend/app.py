import os
import re
from mailjet_rest import Client
import jwt
import os
import datetime
import json
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from functools import wraps
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc, func, text
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.types import Text
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from flask import render_template
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static') 
CORS(app, origins=["https://www.durb.ca", "https://localhost:8080", "https://localhost:8081"], allow_headers=["Content-Type"])
app.config['SECRET_KEY'] = 'your_secret_key'

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

if config.DB_CONNECTED:
    db_path = os.path.join('/app/game_data', 'game.db')
    if config.ENV == "PROD":
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
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

    class GameHistory(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        game_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
        usernames = db.Column(Text, nullable=False)
        user_ranks = db.Column(Text, nullable=False)

        def __init__(self, usernames, user_ranks):
            self.usernames = json.dumps(usernames)
            self.user_ranks = json.dumps(user_ranks)

        @property
        def usernames_list(self):
            return json.loads(self.usernames)

        @property
        def user_ranks_list(self):
            return json.loads(self.user_ranks)


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

s = URLSafeTimedSerializer(app.config['SECRET_KEY']) 

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
            return jsonify({'message': 'Login Token has expired!'}), 401
        except InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500
        
        return f(current_user, *args, **kwargs)
    
    return decorated
@app.after_request

def after_request(response):
    # Get the origin of the request
    origin = request.headers.get('Origin')

    # List of allowed origins
    allowed_origins = ["https://www.durb.ca", "https://localhost:8080", "https://localhost:8081"]

    # Add CORS headers only if the request's origin is in the allowed list
    if origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS,PUT,DELETE')
    
    return response

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS':
        return '', 200  # CORS preflight request
    data = request.json
    login_identifier = data.get('username').lower()  # This could be either username or email
    password = data.get('password')

    if not login_identifier or not password:
        return jsonify({"message": "Missing login identifier or password"}), 400

    if not config.DB_CONNECTED:
        if login_identifier.lower() in ('default', 'other'):
            token = jwt.encode({
                'user': login_identifier,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72),  # Token expires in 72 hours
                'display_name': login_identifier  # For non-DB users, use login identifier as display name
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
    username = data.get('username').lower()
    email = data.get('email').lower()  # Email is received and will be used to send welcome email
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

    return jsonify({"success": True, "message": "Please follow the confirmation email sent to: {} (check spam mail). Note that it can take a while for emails to deliver. ".format(email)}), 200

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
    return render_template('email_confirmation.html', status='confirmed')



@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    username = data.get('username').lower() # email or username
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

def send_mailjet_email(to_email, to_name, subject, text_content, html_content=None, cc_email=None):
    mailjet = Client(auth=(config.MJ_APIKEY_PUBLIC, config.MJ_APIKEY_PRIVATE), version='v3.1')
    message = {
        "From": {
            "Email": config.EMAIL_FROM,
            "Name": "Durb Game"
        },
        "To": [
            {
                "Email": to_email,
                "Name": to_name
            }
        ],
        "Subject": subject,
        "TextPart": text_content,
        "HTMLPart": html_content if html_content else None
    }
    
    if cc_email:
        message["Cc"] = [{"Email": cc_email}]
    
    data = {'Messages': [message]}
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()


def send_confirmation_email(user_email, link):
    subject = "Confirm Your Durb Game Account"
    text_content = f'''Welcome to Durb Game!

    Please confirm your account by clicking the following link:
    {link}

    If you didn't create an account with us, you can safely ignore this email.

    Best regards,
    The Durb Game Team'''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirm Your Durb Game Account</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Welcome to Durb Game!</h2>
            <p>Thank you for creating an account with us. To get started, please confirm your email address by clicking the button below:</p>
            <a href="{link}" class="button">Confirm Your Account</a>
            <p>If the button doesn't work, you can also copy and paste the following link into your browser:</p>
            <p>{link}</p>
            <p>If you didn't create an account with us, you can safely ignore this email.</p>
            <p>Best regards,<br>The Durb Game Team</p>
        </div>
    </body>
    </html>
    '''
    
    status_code, response = send_mailjet_email(user_email, user_email, subject, text_content, html_content)
    
    if status_code == 200:
        return "Confirmation email sent successfully!"
    else:
        print(f"Failed to send confirmation email: {response}")
        return "Error sending confirmation email."

def send_reset_email(user_email, link):
    subject = "Reset Your Durb Game Password"
    text_content = f'''You have requested to reset your Durb Game password.

    To reset your password, please click on the following link:
    {link}

    This link will expire in 5 minutes.

    If you didn't request a password reset, please ignore this email. Your account remains secure.

    Best regards,
    The Durb Game Team'''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Durb Game Password</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 15px;
            }}
            .warning {{
                color: #ff0000;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Reset Your Durb Game Password</h2>
            <p>You have requested to reset your Durb Game password.</p>
            <p>To reset your password, please click the button below:</p>
            <a href="{link}" class="button">Reset Password</a>
            <p>If the button doesn't work, you can also copy and paste the following link into your browser:</p>
            <p>{link}</p>
            <p><strong>This link will expire in 5 minutes.</strong></p>
            <p class="warning">If you didn't request a password reset, please ignore this email. Your account remains secure.</p>
            <p>Best regards,<br>The Durb Game Team</p>
        </div>
    </body>
    </html>
    '''
    
    status_code, response = send_mailjet_email(user_email, user_email, subject, text_content, html_content)
    
    if status_code == 200:
        return "Password reset email sent successfully!"
    else:
        print(f"Failed to send password reset email: {response}")
        return "Error sending password reset email."

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
            # Use a SQL query to get the most recent game containing the exact username
            query = text("""
                SELECT * FROM game_history
                WHERE json_array_length(usernames) > 0
                AND usernames LIKE :username
                ORDER BY game_date DESC
                LIMIT 1
            """)
            
            most_recent_game = db.session.execute(query, {'username': f'%"{user.username}"%'}).fetchone()

            last_game_data = None
            if most_recent_game:
                usernames = json.loads(most_recent_game.usernames)
                user_ranks = json.loads(most_recent_game.user_ranks)
                
                if user.username in usernames:  # Extra check to ensure exact match
                    last_game_data = {
                        "game_id": most_recent_game.id,
                        "game_date": most_recent_game.game_date.format(),
                        "players": []
                    }
                    for username, rank in zip(usernames, user_ranks):
                        player_data = {
                            "username": username,
                            "rank": int(rank),
                            "is_current_user": (username == user.username)
                        }
                        last_game_data["players"].append(player_data)

                    # Sort players by rank
                    last_game_data["players"].sort(key=lambda x: x["rank"])

            return jsonify({
                "userName": user.username,
                "displayName": user.display_name,
                "email": user.email,
                "abilities": user_decks(current_user),
                "elo": user.elo,
                "last_game": last_game_data
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
            "last_game": {
                "game_id": 12345,
                "game_date": "2023-07-23T14:30:00",
                "players": [
                    {"username": "Current-User", "rank": 1, "is_current_user": True},
                    {"username": "Player1", "rank": 2, "is_current_user": False},
                    {"username": "Player3", "rank": 3, "is_current_user": False},
                    {"username": "Player4", "rank": 4, "is_current_user": False}
                ]
            }
        })

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    user_email = data.get('userEmail')
    message_body = data.get('message')

    if not user_email or not message_body:
        return jsonify({"error": "Missing userEmail or message"}), 400
    
    if not re.match(EMAIL_REGEX, user_email):
        return jsonify({"error": "Invalid email format"}), 400

    try:
        # Send email to the main recipient with CC to the user
        send_mailjet_email(
            to_email='lavine.software@gmail.com',
            to_name="Lavine Software",
            subject="New Message from Contact Form",
            text_content=message_body,
            cc_email=user_email
        )
        return jsonify({"success": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_display_name', methods=['POST'])
@token_required
def update_display_name(current_user):
    if config.DB_CONNECTED:
        data = request.json
        display_name = data.get('newDisplayName')
        user = User.query.filter_by(username=current_user).first()
        if user:
            user.display_name = display_name
            db.session.commit()
            return jsonify({"success": True, "message": "Display name updated successfully"}), 200
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    else:
        return jsonify({"success": False, "message": "Database not connected"}), 500


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
            description = ability.get('description', "")
            if ability['name'] in current_cards:
                # Update existing card
                current_cards[ability['name']].count = ability['count']
                current_cards[ability['name']].description = description
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
    
# get user's display name
@app.route('/get_display_name', methods=['POST'])
def get_display_name():
    data = request.json
    token = data.get('token')
    
    if not token:
        return jsonify({"display_name": "guest"})
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded['user']
        
        if config.DB_CONNECTED:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.display_name != "Not Yet Specified":
                    return jsonify({"display_name": user.display_name})
                else:
                    return jsonify({"display_name": user.username})
        else:
            return jsonify({"display_name": username})
        
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({"display_name": "guest"})
    
def username_to_elo(name: str):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=name).first()
        return user.elo if user else 1100  # Default ELO if user not found
    else:
        dummy = {"other": 1200, "default": 1300}
        return dummy.get(name, 1100)  # Def
    
SPAWN_CODE = 115
FREEZE_CODE = 102
BRIDGE_CODE = 97
D_BRIDGE_CODE = 100
ZOMBIE_CODE = 122
RAGE_CODE = 114
BURN_CODE = 98
NUKE_CODE = 110
POISON_CODE = 112
CAPITAL_CODE = 99
CANNON_CODE = 101
PUMP_CODE = 117
MINI_BRIDGE_CODE = 109
    
@app.route('/settings/Royale', methods=['GET'])
def get_royale_settings():
    settings = {
        "ability_type": "elixir",
        "elixir_cap": 8,
        "elixir_rate": 4,
        "growth_rate": 0.13,
        "transfer_rate": 0.012,
        "main_time": 420,
        "overtime": 60,
        "full_size": 200,
        "accessible_percentage": 2/5,
        "walls": True,
        "wall_counts": [2, 2, 1, 2],
        'iterative_make_accessible': True,
        "accessibility_times": [300],
        "starting_structures": False,
        "attack_type": "neighbor",
        "bridge_burn": False,
        "bridge_from_port_needed": False,
        "deck_size": 5,
        "forced_deck": True,
        "deck": [FREEZE_CODE, D_BRIDGE_CODE, BRIDGE_CODE, RAGE_CODE, NUKE_CODE]
    }
    return jsonify(settings)

@app.route('/settings/Original', methods=['GET'])
def get_og_settings():
    settings = {
        "ability_type": "credits",
        "credit_cap": 22,
        "growth_rate": 0.15,
        "transfer_rate": 0.012,
        "main_time": 390,
        "overtime": 90,
        "full_size": 250,
        "accessible_percentage": 4/7,
        "walls": False,
        'iterative_make_accessible': False,
        "starting_structures": True,
        "starting_land_capitals": 3,
        "starting_island_capitals": 1,
        "attack_type": "structure_range",
        "bridge_burn": False,
        "bridge_from_port_needed": False,
        "deck_size": 5,
        "forced_deck": False,
    }
    return jsonify(settings)
    
@app.route('/abilities/Royale', methods=['GET'])
def get_royale_abilities():
    abilities = [
        {
            "name": "Bridge", 
            "cost": 4,
            "description": "Create a one-way bridge"
        },
        {
            "name": "D-Bridge", 
            "cost": 3,
            "description": "Create a two-way bridge with"
        },
        {
            "name": "Freeze", 
            "cost": 2,
            "description": "Convert edge to one-way"
            
        },
        {
            "name": "Rage", 
            "cost": 5,
            "description": "Increase energy transfer speed"
        },
        {
            "name": "Nuke", 
            "cost": 6,
            "description": "Destroy nearby dot and its bridges"
        },
        {
            "name": "Over-Grow",
            "cost": 4,
        },
        {
            "name": "Wall-Breaker",
            "cost": 3,
        },
        {
            "name": "Poison",
            "cost": 5,
        }
    ]
    return jsonify({"abilities": abilities, "options": 6})
    
@app.route('/abilities/Original', methods=['GET'])
def get_og_abilities():
    abilities = [
        {
            "name": "Mini-Bridge", 
            "cost": 1,
            "description": "Create a two-way bridge with limited range"
        },
        {
            "name": "Spawn", 
            "cost": 1,
            "description": "Claim unowned node anywhere"
        },
        {
            "name": "Freeze", 
            "cost": 1,
            "description": "Convert edge to one-way"
            
        },
        {
            "name": "Burn", 
            "cost": 1,
            "description": "Remove ports from node"
        },
        {
            "name": "Wormhole",
            "cost": 1,
            "description": "Teleport structure to another node"
        },
        {
            "name": "Zombie",
            "cost": 3,
            "description": "Create controllable apocalypse"
        },
        {
            "name": "Nuke", 
            "cost": 3,
            "description": "Destroy node and edges (capital needed)"
        },
        {
            "name": "Bridge", 
            "cost": 2,
            "description": "Create a one-way bridge"
        },
        {
            "name": "Poison", 
            "cost": 2,
            "description": "Spreadable effect to shrink nodes"
        },
        {
            "name": "Rage", 
            "cost": 2,
            "description": "Increase energy transfer speed"
        },
        # {
        #     "name": "D-Bridge", 
        #     "cost": 2,
        #     "description": "Create a two-way bridge"
        # },
        {
            "name": "Over-Grow",
            "cost": 2,
            "description": "nodes can grow to any size for short period"
        },
        {
            "name": "Capital", 
            "cost": 2,
            "description": "Create a capital" 
        },
        {
            "name": "Pump", 
            "cost": 3,
            "description": "Store energy to replenish abilities"
        },
        {
            "name": "Cannon", 
            "cost": 4,
            "description": "Shoot energy at nodes"
        }
    ]
    return jsonify({"abilities": abilities, "credits": 22, "options": 5})


@app.route('/save_game', methods=['POST'])
def save_game():
    data = request.json
    ordered_tokens = data.get("ordered_players")

    if not ordered_tokens:
        return jsonify({"error": "Missing ordered players"}), 400
    
    if config.DB_CONNECTED:
        usernames = []
        user_ranks = []
        for rank, token in enumerate(ordered_tokens, start=1):
            username = token_to_username(token)
            # username = token
            user = User.query.filter_by(username=username).first()
            if user:
                usernames.append(username)
            
            else:
                usernames.append("Guest")
            user_ranks.append(rank)
        
        new_game = GameHistory(usernames=usernames, user_ranks=user_ranks)
        db.session.add(new_game)
        db.session.commit()

        return update_elo()
    
    else:
        return update_elo()


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
        # Subquery to count the number of games each user has participated in
        subquery = (
            db.session.query(User.username, func.count(GameHistory.id).label('game_count'))
            .join(GameHistory, GameHistory.usernames.contains(User.username))
            .group_by(User.username)
            .subquery()
        )

        # Query to filter users based on game_count and email confirmation
        confirmed_users = (
            db.session.query(User)
            .join(subquery, User.username == subquery.c.username)
            .filter(User.email_confirm == True, subquery.c.game_count >= 3)
            .order_by(desc(User.elo))
            .all()
        )
        leaderboard = [
            {
                "userName": user.username,
                "displayName": user.display_name,
                "elo": user.elo
            } 
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


@app.route('/current-user', methods=['GET'])
@token_required
def get_current_user(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            games = GameHistory.query.filter(GameHistory.usernames.like(f'%{user.username}%')).order_by(GameHistory.game_date.desc()).limit(3).all()
            gameCount = len(games)
            return jsonify({
                "username": user.username,
                "gameCount" : gameCount
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        # If DB is not connected, return the username from the token
        return jsonify({
            "username": current_user,
            "gameCount": 3
        }), 200


@app.route('/user/<string:username>', methods=['GET'])
def get_user_details(username):
    if not config.DB_CONNECTED:
        return jsonify({"error": "Database not connected"}), 500

    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        deck = Deck.query.filter_by(user_id=user.id).first()
        deck_cards = []
        if deck:
            deck_cards = DeckCard.query.filter_by(deck_id=deck.id).all()
        
        response = {
            "username": user.username,
            "displayName": user.display_name,
            "elo": user.elo,
            "deck": [{"name": card.ability, "count": card.count} for card in deck_cards]
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/match-history', methods=['GET'])
@token_required
def get_match_history(current_user):
    if config.DB_CONNECTED:
        user = User.query.filter_by(username=current_user).first()
        if user:
            # Use a SQL query to filter games containing the exact username
            query = text("""
                SELECT * FROM game_history
                WHERE json_array_length(usernames) > 0
                AND usernames LIKE :username
                ORDER BY game_date DESC
                LIMIT 20
            """)
            
            games = db.session.execute(query, {'username': f'%"{user.username}"%'}).fetchall()

            match_history = []
            for game in games:
                usernames = json.loads(game.usernames)
                user_ranks = json.loads(game.user_ranks)
                if user.username in usernames:  # Extra check to ensure exact match
                    game_data = {
                        "game_id": game.id,
                        "game_date": game.game_date.format(),
                        "players": []
                    }
                    for username, rank in zip(usernames, user_ranks):
                        player_data = {
                            "username": username,
                            "rank": int(rank),
                            "is_current_user": (username == user.username)
                        }
                        game_data["players"].append(player_data)
                    game_data["players"].sort(key=lambda x: x["rank"])
                    match_history.append(game_data)
            
            return jsonify({"match_history": match_history})
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        # Return dummy data for testing when DB is not connected
        return jsonify({
            "match_history": [
                {
                    "game_id": i,
                    "game_date": (datetime.datetime.now() - datetime.timedelta(days=i)).isoformat(),
                    "players": [
                        {"username": "Current-User", "rank": 1, "is_current_user": True},
                    ] + [
                        {"username": f"Player{j}", "rank": j+1, "is_current_user": False} for j in range(1, 4)
                    ]
                } for i in range(1, 21)
            ]
        })

if __name__ == '__main__':
    if config.ENV == "PROD":
        certfile = "fullchain.pem"
        keyfile = "privkey.pem"
        app.run( debug=False, host='0.0.0.0', port=5001,ssl_context=(certfile, keyfile))
    else:
        app.run( debug=False, host='0.0.0.0', port=5001)
    
