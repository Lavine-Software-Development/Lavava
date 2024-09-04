from flask import Blueprint, jsonify, request

from chatbot import Chatbot

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

chat_bot = Chatbot()

@chat_bp.route('/')
def get_chat():
    return chat_bot.get_chat()

@chat_bp.route('/', methods=["POST"])
def send_chat():
    # Access the raw text from the request body
    message = request.get_data(as_text=True)
    
    if not message:
        return jsonify({"error": "No message provided"}), 400  # Return 400 if no body
    
    response = chat_bot.send_message(message)
    
    return jsonify({'response': response}), 200

@chat_bp.route('/reset', methods=["DELETE"])
def reset_chat():
    chat_bot.reset_chat()
    return jsonify({'message': 'chat successfully reset'}), 200