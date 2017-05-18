import abc
import logging
from flask import jsonify

logger = logging.getLogger(__name__)


class HttpException(Exception, metaclass=abc.ABCMeta):
    CODE = 0
    description = None


class HttpError(HttpException):
    CODE = 400
    description = ('The browser (or proxy) sent a request that this server could ' \
                   'not understand.')


class Unauthorized(HttpException):
    CODE = 401
    description = ('The server could not verify that you are authorized to access ' \
                   'the URL requested.  You either supplied the wrong credentials (e.g. ' \
                   'a bad password), or your browser doesn\'t understand how to supply ' \
                   'the credentials required.')


def error_handler(f):
    def wrapper (*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except HttpException as e:
            body = {
                'message':str(e),
                'code':e.code
            }
        except Exception as e:
            body = {
                'message':str(e),
                'code':500
            }
            logging.exception(body['message'])
            return jsonify(body),500
    return wrapper
