from flask import Flask, request
from flask import jsonify, json
from storage import Storage
from exceptions import error_handler
from authentication import auth
app = Flask(__name__)


@app.route("/tweets/", methods=["GET"])
@error_handler
def get_tweets():
    """
    Display all tweets. 
    """
    tweets = Storage.get_tweets()
    return (
        (jsonify([tweet.to_dict() for tweet in tweets]), 200)
        if len(tweets) > 0 else ("No tweets", 404)
    )


@app.route("/tweets/<int:tweet_id>", methods=["GET"])
#@error_handler
def get_tweet(tweet_id):
    """
    Display single tweet. 
    """
    tweet = Storage.get_tweet(tweet_id)
    return (jsonify(tweet.to_dict()), 200) if tweet else ("Not found", 404)


@app.route("/tweets/", methods=['POST'])
#@error_handler
def post_tweet():
    """
    Save tweet to storage. 
    """
    if not request.get_json():
        return "Missing tweet", 400
    tweet = Storage.post_tweet(json.loads(request.get_json())["tweet"])
    return jsonify(tweet), 201


@app.route("/tweets/<int:tweet_id>", methods=['DELETE'])
#@error_handler
@auth
def del_tweet(tweet_id):
    """
    Delete tweet with given id 
    """
    return jsonify(Storage.del_tweet(tweet_id)), 204


if __name__ == "__main__":
    Storage.create_db_table()
    app.run(host='0.0.0.0')
