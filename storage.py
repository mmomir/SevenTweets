class Storage(object):

    _tweets = []
    _tweet_count  = 0
    _server_name = "Milos"


    @classmethod
    def get_tweets(cls):
        """
        Return all tweets.
        """
        return cls._tweets

    @classmethod
    def get_tweet(cls,tweet_id):
        """
        Return single tweet. 
        """
        for tweet in cls._tweets:
            if tweet['id'] == tweet_id:
                return tweet
        else:
            return None

    @classmethod
    def post_tweet(cls, body):
        """
        Method used to create tweet
        """
        cls._tweet_count += 1
        tweet = {"id": cls._tweet_count,"name": cls._server_name, "tweet": body}
        cls._tweets.append(tweet)
        return "Ok"

    @classmethod
    def del_tweet(cls, tweet_id):
        """
        Method used to delete tweet 
        """
        n = len(cls._tweets)
        for tweet in cls._tweets:
            if tweet['id'] == tweet_id:
                del cls._tweets[cls._tweets.index(tweet)]

        if n == len(cls._tweets):
            print("No tweet with ID {}".format(tweet_id))
            raise IndexError ("No tweet with ID {}".format(tweet_id))
