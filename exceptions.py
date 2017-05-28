import abc
import logging
from flask import jsonify
from functools import wraps

logger = logging.getLogger(__name__)


class HttpException(Exception, metaclass=abc.ABCMeta):
    default_description = ''
    CODE = 0

    def __init__(self, message=None):
        if message:
            self.message = message
        # else:
        self.description = self.__class__.default_description


class HttpError(HttpException):

    """
    *400* `Bad Request`
    Raise if the browser sends something to the application the application
    or server cannot handle.
    """

    CODE = 400
    default_description = ('The browser sent a request that this server could '
                           'not understand.')


class Unauthorized(HttpException):

    """
    *401* `Unauthorized`
    Raise if the user is not authorized. 
    """

    CODE = 401
    default_description = ('The server could not verify that you are authorized to access '
                           'the URL requested.  You either supplied the wrong credentials (e.g. '
                           'a bad password), or your browser doesn\'t understand how to supply '
                           'the credentials required.')


class Forbidden(HttpException):

    """
    *403* `Forbidden`
    Raise if the user doesn't have the permission for the requested resource
    but was authenticated.
    """

    CODE = 403
    default_description = (
        'You don\'t have the permission to access the requested resource. '
        'It is either read-protected or not readable by the server.')


class NotFound(HttpException):

    """
    *404* `Not Found`
    Raise if a resource does not exist and never existed.
    """
    CODE = 404
    default_description = (
        'The requested URL was not found on the server.  '
        'If you entered the URL manually please check your spelling and '
        'try again')


class RequestTimeout(HttpException):

    """
    *408* `Request Timeout`
    Raise to signalize a timeout.
    """
    CODE = 408
    default_description = (
        'The server closed the network connection because the browser '
        'didn\'t finish the request within the specified time.')


def error_handler(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            print("success")
            return f(*args, **kwargs)
        except HttpException as e:
            body = {
                'message': e.message,
                'code': e.CODE,
                'description': e.description
            }
            logging.exception(body['message'])
            return jsonify(body), e.CODE
        except Exception as e:
            body = {
                'message': str(e),
                'code': 500
            }
            logging.exception(body['message'])
            return jsonify(body), 500
    return wrapper
