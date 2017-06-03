"""
Module that defines Tweet model
"""


class Tweet(object):

    def __init__(self, id=None, name=None, tweet=None, created_at = None, type= None):
        self.id = id
        self.name = name
        self.tweet = tweet
        self.created_at = created_at
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tweet': self.tweet,
            'created_at': self.created_at,
            'type': self.type
        }

    @classmethod
    def from_dict(cls, data):
        return Tweet(**data)
