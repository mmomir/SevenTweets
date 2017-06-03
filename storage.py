import functools
from datetime import datetime
import pg8000
from config import Config
from tweet import Tweet
from node import Node


def uses_db(f):
    @functools.wraps(f)
    def wrapper(cls, *args, **kwargs):
        cursor = cls._conn.cursor()
        try:
            res = f(cls, cursor, *args, **kwargs)
        except Exception as e:
            cursor.rollback()
            cursor.close()
            cls._conn.commit()
            raise e

        cursor.close()
        cls._conn.commit()
        return res
    return wrapper


class Storage(object):
    print (Config.DB_CONFIG)
    _conn = pg8000.connect(**Config.DB_CONFIG)

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
#        query_str = 'SELECT * from tweets WHERE id = {id}'.format(id=tweet_id)
        cursor.execute("SELECT * FROM tweets WHERE id = %s",(tweet_id,))
        tweet_data = cursor.fetchone()
        if tweet_data:
            return Tweet(*tweet_data)
        else:
            return None

    @classmethod
    @uses_db
    def get_nodes(cls,cursor):
        cursor.execute("SELECT * FROM network")
        nodes = [Node(*data) for data in cursor.fetchall()]
        return nodes

    @classmethod
    @uses_db
    def get_node(cls, cursor, name):
        """
        Return single node. 
        """
#        query_str = 'SELECT * from tweets WHERE id = {id}'.format(id=tweet_id)
        cursor.execute("SELECT * FROM network WHERE name = %s", (name,))
        name_data = cursor.fetchone()
        if name_data:
            return Tweet(*name_data)
        else:
            return None

    @classmethod
    @uses_db
    def post_tweet(cls, cursor, tweet):
        """
        Method used to create tweet
        """
#        query_id = 'SELECT max(id) from tweets'
#        cursor.execute(query_id)
#         cls.tweet_id += 1
        # query_str = 'INSERT INTO tweets (name,tweet) VALUES (%s,%s) RETURING id, name, tweet'
        # id=cls.tweet_id, name=cls._server_name, tweet=body)
#        cursor.execute('INSERT INTO (name, tweet) VALUES (%s,%s) RETURNING id, name, tweet', (Config.NAME, Tweet.tweet))
#         tweet = "post"
        cursor.execute('INSERT INTO tweets (name, tweet, created_at, type) VALUES (%s,%s,%s,%s) '
                       'RETURNING id, name, tweet, created_at, type',
                       (Config.NAME, tweet.tweet, datetime.now(), tweet.type))
        data = cursor.fetchone()
        new_tweet = Tweet(*data)
        return new_tweet

    @classmethod
    @uses_db
    def post_registry(cls, cursor, node):
        cursor.execute('SELECT id FROM network WHERE server_address = %s ',(node.server_address,))
        result = cursor.fetchone()
        if not result:
            cursor.execute('INSERT INTO network (name, server_address) VALUES (%s,%s) '
                           'RETURNING id, name, server_address',
                           (node.name, node.server_address))

        cursor.execute("SELECT * from network")
        nodes = [Node(*data) for data in cursor.fetchall()]
        return nodes

    @classmethod
    @uses_db
    def del_tweet(cls, cursor, tweet_id):
        """
        Method used to delete tweet 
        """
        tweet = cls.get_tweet(tweet_id=tweet_id)

        # if tweet:
        # query_str = "DELETE FROM tweets WHERE id=%s"
        cursor.execute("DELETE FROM tweets WHERE id=%s",(tweet_id,))
        return 'OK'
        # else:
        #     print("No tweet with ID {}".format(tweet_id))
        #     raise IndexError("No tweet with ID {}".format(tweet_id))

    @classmethod
    @uses_db
    def del_node(cls, cursor, name):
        """
        Method used to delete tweet 
        """
        node = cls.get_node(name=name)

        # if tweet:
        # query_str = "DELETE FROM tweets WHERE id=%s"
        cursor.execute("DELETE FROM network WHERE name=%s",(name,))
        return 'OK'


    @classmethod
    @uses_db
    def put_tweet(cls, cursor, tweet_id, tweet):
        """
        Method used to put tweet 
        """
        cursor.execute('INSERT INTO tweets (id, name, tweet, created_at, type)) VALUES (%s,%s,%s,%s,%s) '
                       'RETURNING id, name, tweet, created_at, type',
                       (tweet_id, Config.NAME, tweet.tweet, datetime.now(),tweet.type))
        data = cursor.fetchone()
        new_tweet = Tweet(*data)
        return new_tweet

    @classmethod
    @uses_db
    def search_tweet(cls, cursor, content, created_from, created_to):
        query = 'SELECT * FROM tweets WHERE true'
        if content and content != '':
            query += ' AND tweet LIKE \'%%{}%%\''.format(content)

        if created_from and isinstance(created_from, datetime):
            query += ' AND created_at >= \'{}\''.format(str(created_from))

        if created_to and isinstance(created_to, datetime):
            query += ' AND created_at <= \'{}\''.format(str(created_to))

        cursor.execute(query)
        tweets = [Tweet(*data) for data in cursor.fetchall()]
        return tweets
