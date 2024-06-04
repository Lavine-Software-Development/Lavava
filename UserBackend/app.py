import jwt
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

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
    if username.lower() == 'default':
        # Create a token
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=72)  # Token expires in 24 hours
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')  # Email is received but not used in logic for simplicity
    password = data.get('password')  # Password is received but not used in logic
    
    if username.lower() == 'default':
        return jsonify({"success": True, "message": "Registration successful"}), 200
    else:
        return jsonify({"success": False, "message": "Registration failed, username must be 'default'"}), 400
    
@app.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if current_user == "default":
        return jsonify({
            "userName": "Default-User",
            "displayName": "John Doe",
            "email": "john.doe@example.com",
            "abilities": ["Bridge", "Freeze", "Poison", "Rage"],
            "elo": 1138,
            "past_games": ["1st", "4th", "2nd"]
        })
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
