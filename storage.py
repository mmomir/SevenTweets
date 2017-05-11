import functools

import pg8000

from config import Config
from tweet import Tweet


def uses_db(f):
    @functools.wraps(f)
    def wrapper(cls, *args, **kwargs):
        cursor = cls._conn.cursor()
        res = f(cls, cursor, *args, **kwargs)
        cursor.close()
        cls._conn.commit()
        return res
    return wrapper


class Storage(object):
    _conn = pg8000.connect(**Config.DB_CONFIG)

    _tweets = []
    _tweet_count = 0
    _server_name = "Milos"

    @classmethod
    @uses_db
    def get_tweets(cls, cursor):
        """
        Return all tweets.
        """
        cursor.execute("SELECT * from tweets")
        tweets = [Tweet(*data) for data in cursor.fetchall()]
        return tweets

    @classmethod
    @uses_db
    def get_tweet(cls, cursor, tweet_id):
        """
        Return single tweet. 
        """
        query_str = 'SELECT * from tweets WHERE id = {id}'.format(id=tweet_id)
        cursor.execute(query_str)
        tweet_data = cursor.fetchone()
        if tweet_data:
            return Tweet(*tweet_data)
        else:
            return None

    @classmethod
    @uses_db
    def post_tweet(cls, cursor, body):
        """
        Method used to create tweet
        """
        query_id = 'SELECT max(id) from tweets'
        cursor.execute(query_id)
        tweet_id = int(cursor.fetchone()) + 1
        query_str = 'INSERT INTO (id, name, tweet) values ({id}, {name}, {tweet})'.format(
            id=tweet_id, name=cls._server_name, tweet=body)
        cursor.execute(query_str)
        return "Ok"

    @classmethod
    @uses_db
    def del_tweet(cls, cursor, tweet_id):
        """
        Method used to delete tweet 
        """
        tweet = cls.get_tweet(tweet_id=tweet_id)

        if tweet:
            query_str = 'DELETE FROM tweets where id={id})'.format(
                id=tweet_id)
            cursor.execute(query_str)
            return 'OK'
        else:
            print("No tweet with ID {}".format(tweet_id))
            raise IndexError("No tweet with ID {}".format(tweet_id))

    @classmethod
    @uses_db
    def create_db_table(cls, cursor):
        """
        Creates tweets table in database.  
        """
        if cls.check_if_table_exist(cursor):
            cursor.execute("CREATE TABLE tweets (id SERIAL, name TEXT, tweet TEXT)")

    @classmethod
    def check_if_table_exist(cls, cursor):
        """
        Check if table tweets exist.  
        """

        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE 'tweets'")
        return int(cursor.fetchone()) == 1