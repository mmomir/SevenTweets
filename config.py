import os
import binascii


def generate_api_token():
    """
    Generates random token.
    """
    return binascii.b2a_hex(os.urandom(15))


class Config(object):
    """
    Global object to hold configuration.
    """
    DB_CONFIG = dict(user=os.environ.get('ST_DB_USER', None),
                     database=os.environ.get('ST_DB_NAME', None),
                     host=os.environ.get('ST_DB_HOST', None),
                     # host=os.environ.get('ST_DB_HOST', '192.168.99.100'),

                     password=os.environ.get('ST_DB_PASS', None),
                     port=int(os.environ.get('ST_DB_PORT', 5432)))
    NAME = os.environ.get('ST_NAME', 'import')
    # TODO: If token is not provided, no one knows it - log it somewhere
    # API_TOKEN = os.environ.get('ST_API_TOKEN', generate_api_token())
    API_TOKEN = '1234'
    ADDRESS = 'import.sedamcvrkuta.com'

    @classmethod
    def address_or_name_not_provided(cls):
        return (
            not cls.ADDRESS or cls.ADDRESS == '' or
            not cls.NAME or cls.NAME == ''
        )

    @classmethod
    def address_not_provided(cls):
        return (
            not cls.ADDRESS or cls.ADDRESS == ''
        )

    @classmethod
    def name_not_provided(cls):
        return (
            not cls.NAME or cls.NAME == ''
        )

