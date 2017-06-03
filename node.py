"""
Module that defines Node model
"""


class Node(object):

    def __init__(self, id=None, name=None, server_address=None):
        self.id = id
        self.name = name
        self.server_address = server_address

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'server_address': self.server_address
        }

    @classmethod
    def from_dict(cls, data):
        return Node(**data)
