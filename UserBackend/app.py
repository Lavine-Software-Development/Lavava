import jwt
import datetime
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from functools import wraps
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

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
    if username.lower() == 'default' or 'other':
        # Create a token
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)  # Token expires in 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    SpecialSym = ["!","%","#","@","$","^","&","*","+","_","-","="]
    data = request.json
    username = data.get('username')
    email = data.get('email')  # Email is received and will be used to send welcome email
    password = data.get('password') # password received and used to check requirements before sending email

    token = s.dumps(email, salt='email-confirm')
    link = url_for('confirm_email', token=token, _external=True)

    if len(password) < 8: # checks for password requirements
        return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400
    if not any(char.islower() for char in password):
        return jsonify({"success": False, "message": "Password must have at least one lowercase letter"}), 400
    if not any(char.isupper() for char in password):
        return jsonify({"success": False, "message": "Password must have at least one uppercase letter"}), 400
    if not any(char.isdigit() for char in password):
        return jsonify({"success": False, "message": "Password must contain a number"}), 400
    if not any(char in SpecialSym for char in password):
        return jsonify({"success": False, "message": "Password must contain a special character"}), 400
    if username.lower() == 'default':
        send_confirmation_email(email, link)  # Send confirm email
        return jsonify({"success": True, "message": "Registration successful. Please follow the confirmation email sent to: {}".format(email)}), 200
    else:
        return jsonify({"success": False, "message": "Registration failed, username must be 'default'"}), 400

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600) # token expires after 1 hour
    except SignatureExpired:
        return '<h1>Email confirmation link expired!</h1>' # token expired
    except:
        return '<h1>Error!</h1>' # other error like incorrect token
    return '<h1>Email Confirmed!</h1>' # set here that email was confirmed in database 

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


@app.route('/user_abilities', methods=['GET'])
@token_required
def get_home(current_user):
    if current_user == "default" or 'other':
        return jsonify({
            "abilities": user_decks(current_user),
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if current_user == "default" or 'other':
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
    if current_user == "default" or 'other':
        return [{"name": "Capital", "count": 1}, {"name": "Cannon", "count": 1}, {"name": "Rage", "count": 2}, {"name": "Poison", "count": 1}]
    else:
        return []
    
def update_elos(elos, k_factor=32):
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

# Test cases
# test_cases = [
#     [1000, 500, 1000],
#     [1000, 1000],
#     [1200, 1250, 1300]
# ]

# for case in test_cases:
#     print(f"Original Elos: {case}")
#     print(f"Updated Elos:  {update_elos(case)}")
#     print()
    
# to be updated with actual db queries


def token_to_username(token: str):
        try:
            return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user']
        except jwt.ExpiredSignatureError:
            return 'Expired token'
        except jwt.InvalidTokenError:
            return 'Invalid token'

def username_to_elo(name: str):
    dummy = {"other": 1200, "default": 1300}
    return dummy[name]
    
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
    ordered_tokens_and_ids = request.json.get("ordered_players")
    tokens = [item[0] for item in ordered_tokens_and_ids]
    ids = [item[1] for item in ordered_tokens_and_ids]

    usernames = [token_to_username(token) for token in tokens]
    old_elos = [username_to_elo(user) for user in usernames]
    new_elos = update_elos(old_elos)

    elo_tuples = {ids[i]: list(zip(old_elos, new_elos))[i] for i in range(len(ids))}
    return jsonify({"new_elos": elo_tuples})


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
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
