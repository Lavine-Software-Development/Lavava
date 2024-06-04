from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
    
@app.route('/profile/<username>')
def get_profile(username):
    print('made it')
    if username == "Default-User":
        print("to the right place")
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
