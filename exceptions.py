import abc
import logging
from flask import jsonify

logger = logging.getLogger(__name__)


class HttpException(Exception, metaclass=abc.ABCMeta):
    CODE = 0
    description = None


class HttpError(HttpException):

    """
    *400* `Bad Request`
    Raise if the browser sends something to the application the application
    or server cannot handle.
    """

    CODE = 400
    description = ('The browser sent a request that this server could ' 
                   'not understand.')


class Unauthorized(HttpException):

    """
    *401* `Unauthorized`
    Raise if the user is not authorized. 
    """

    CODE = 401
    description = ('The server could not verify that you are authorized to access '
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
    description = (
        'You don\'t have the permission to access the requested resource. '
        'It is either read-protected or not readable by the server.')


class NotFound(HttpException):

    """
    *404* `Not Found`
    Raise if a resource does not exist and never existed.
    """

    CODE = 404
    description = (
        'The requested URL was not found on the server.  '
        'If you entered the URL manually please check your spelling and '
        'try again')


class RequestTimeout(HttpException):

    """
    *408* `Request Timeout`
    Raise to signalize a timeout.
    """
    CODE = 408
    description = (
        'The server closed the network connection because the browser '
        'didn\'t finish the request within the specified time.')


def error_handler(f):

    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HttpException as e:
            body = {
                'message': str(e),
                'code': e.CODE,
                'description': e.description
            }
        except Exception as e:
            body = {
                'message': str(e),
                'code': 500
            }
            logging.exception(body['message'])
            return jsonify(body), 500
    return wrapper
