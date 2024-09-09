import logging
from flask import Blueprint, jsonify, request
import sys

from .chatbot import Chatbot
from util import token_required


chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

user_chats: dict[str, Chatbot] = {}

@chat_bp.route('/')
@token_required
def get_chat(current_user):
    if current_user not in user_chats:
        user_chats[current_user] = Chatbot()

    return user_chats[current_user].get_chat()

@chat_bp.route('/', methods=["POST"])
@token_required
def send_chat(current_user):
    if current_user not in user_chats:
        user_chats[current_user] = Chatbot()
    
    message = request.get_data(as_text=True)
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    response = user_chats[current_user].send_message(message)
    
    return jsonify({'response': response}), 200

@chat_bp.route('/reset', methods=["DELETE"])
@token_required
def reset_chat(current_user):
    if current_user not in user_chats:
        user_chats[current_user] = Chatbot()
    user_chats[current_user].reset_chat()
    return jsonify({'message': 'chat successfully reset'}), 200