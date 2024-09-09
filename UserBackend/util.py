from functools import wraps
from flask import jsonify, request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
from config import config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]  # Assuming bearer token is used
            except IndexError:
                return jsonify({"message": "Invalid Authorization header format!"}), 401

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
            current_user = data["user"]
        except ExpiredSignatureError:
            return jsonify({"message": "Login Token has expired!"}), 401
        except InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500

        return f(current_user, *args, **kwargs)

    return decorated