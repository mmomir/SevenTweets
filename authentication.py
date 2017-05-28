from flask import request
from functools import wraps
from config import Config
import exceptions

API_TOKEN_HEADER = 'X-Api-Token'


def auth(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if (
            API_TOKEN_HEADER not in request.headers or
            request.headers.get(API_TOKEN_HEADER) != Config.API_TOKEN
        ):
            raise exceptions.Unauthorized(
                "Token ({}) is not valid.".format(
                    request.headers.get(API_TOKEN_HEADER))
            )
        return f(*args, **kwargs)
    return wrapper
