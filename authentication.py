from flask import request, jsonify
from functools import wraps
from config import Config

API_TOKEN_HEADER = 'X-Api-Token'


def auth(f):

    @wraps(f)
    def wrapper(*args, **kvargs):
        if request.headers.get(API_TOKEN_HEADER) != Config.API_TOKEN:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kvargs)
    return wrapper