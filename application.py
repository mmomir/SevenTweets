from flask import Flask, request
from flask import jsonify
from storage import Storage
from exceptions import error_handler
from authentication import auth
from tweet import Tweet
import exceptions
app = Flask(__name__)


@app.route("/tweets/", methods=["GET"])
@error_handler
@auth
def get_tweets():
    """
    Display all tweets. 
    """
    tweets = Storage.get_tweets()
    if len(tweets) == 0:
        raise exceptions.NotFound(message="Not found tweets")
    return (
        (jsonify([tweet.to_dict() for tweet in tweets]), 200)
    )


@app.route("/tweets/<int:tweet_id>", methods=["GET"])
@error_handler
@auth
def get_tweet(tweet_id):
    """
    Display single tweet. 
    """
    tweet = Storage.get_tweet(tweet_id)
    if not tweet:
        raise exceptions.NotFound(message="Not found tweet with id {}".format(tweet_id))
    return (jsonify(tweet.to_dict()), 200) if tweet else ("Not found", 404)


@app.route("/tweets/", methods=['POST'])
@error_handler
@auth
def post_tweet():
    """
    Save tweet to storage. 
    """
    if not request.get_json() or 'tweet' not in request.get_json():
        raise exceptions.HttpError(message="No tweet info in body")

    post_tweet = Tweet(
        id=None,
        name=None,
        tweet=request.get_json()["tweet"]
    )

    tweet = Storage.post_tweet(tweet=post_tweet)
    return jsonify(tweet.to_dict()), 201


@app.route("/tweets/<int:tweet_id>", methods=['DELETE'])
@error_handler
@auth
def del_tweet(tweet_id):
    """
    Delete tweet with given id 
    """
    tweet = Storage.get_tweet(tweet_id)
    if not tweet:
        raise exceptions.NotFound(message="Not found tweet with id {}".format(tweet_id))
    return jsonify(Storage.del_tweet(tweet_id)), 204


if __name__ == "__main__":
    Storage.create_db_table()
    app.run(host='0.0.0.0')
