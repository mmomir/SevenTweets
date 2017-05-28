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
        cursor.execute('INSERT INTO tweets (name,tweet) VALUES (%s,%s) RETURNING id, name, tweet',(Config.NAME, tweet.tweet))
        data = cursor.fetchone()
        new_tweet = Tweet(*data)
        return new_tweet

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
    def create_db_table(cls, cursor):
        """
        Creates tweets table in database.  
        """
        if not cls.check_if_table_exist(cursor):
            cursor.execute("CREATE TABLE tweets (id SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL, tweet TEXT)")

    @classmethod
    def check_if_table_exist(cls, cursor):
        """
        Check if table tweets exist.  
        """

        exists = False
        cursor.execute("SELECT count(*) FROM information_schema.tables WHERE table_name LIKE 'tweets'")
        for count in cursor.fetchone():
            exists = count == 1

        return exists
