from flask import Flask, request
from flask import jsonify, json
from storage import Storage


app = Flask(__name__)

@app.route("/tweets/", methods=["GET"])
def get_tweets():
    """
    Display all tweets. 
    """
    tweet = Storage.get_tweets()
    return jsonify(tweet) if tweet else ("No tweets", 404)

@app.route("/tweets/<int:tweet_id>", methods = ["GET"])
def get_tweet(tweet_id):
    """
    Display single tweet. 
    """
    tweet = Storage.get_tweet(tweet_id)
    return jsonify(tweet) if tweet else ("Not found", 404)


@app.route("/tweets/", methods=['POST'])
def post_tweet():
    """
    Save tweet to storage. 
    """
    if not request.get_json():
        return ("Missing tweet", 400)
    tweet = Storage.post_tweet(json.loads(request.get_json())["tweet"])
    return (jsonify(tweet),201)

@app.route("/tweets/<int:tweet_id>", methods=['DELETE'])
def del_tweet(tweet_id):
    """
    Delete tweet with given id 
    """
    return (jsonify(Storage.del_tweet(tweet_id)), 204)

if __name__ == "__main__":
    app.run()