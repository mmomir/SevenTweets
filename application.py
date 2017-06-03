from flask import Flask, request
from flask import jsonify
from storage import Storage
from exceptions import error_handler
from authentication import auth
from tweet import Tweet
from node import Node
import exceptions
import requests
import json
from config import Config
from datetime import datetime
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
        tweet=request.get_json()["tweet"],
        created_at=None,
        type = 'original'
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


@app.route("/tweets/<int:tweet_id>", methods=['PUT'])
@error_handler
@auth
def put_tweet(tweet_id):
    """
    Put tweet with given id 
    """
    if not request.get_json() or 'tweet' not in request.get_json():
        raise exceptions.HttpError(message="No tweet info in body")
    put_tweet = Tweet(
        id=tweet_id,
        name=None,
        tweet=request.get_json()["tweet"],
        created_at=None,
        type='original'
    )
    tweet = Storage.put_tweet(tweet_id, tweet=put_tweet)
    return jsonify(tweet.to_dict()), 201


@app.route("/registry", methods=['POST'])
def post_registry():
    if not request.get_json() or 'server_address' not in request.get_json():
        raise exceptions.HttpError(message="No server address info in body")

    new_node = Node(
        id=None,
        name=request.get_json()["name"],
        server_address=request.get_json()["server_address"]
    )

    nodes = Storage.post_registry(node=new_node)
    return jsonify([node.to_dict() for node in nodes]), 201


@app.route("/registry/<name>", methods=['DELETE'])
def del_registry(name):
    """
    Delete node with given name
    """
    node_del = Storage.get_node(name)
    if not node_del:
        raise exceptions.NotFound(message="Not found node with name: {}".format(name))
    return jsonify(Storage.del_node(name)), 204


@app.route("/join_network/", methods=['POST'])
@error_handler
def join_net():
    if not request.get_json():
        raise exceptions.HttpError(message="No info in body")

    json_body = request.get_json()

    local_node = json_body.get('local_node', None)

    if not local_node or not isinstance(local_node, dict):
        if Config.address_or_name_not_provided():
            raise exceptions.HttpError(
                message="No name or address provided."
            )

    local_node_address = local_node.get('server_address', None)

    if(
        (
            not local_node_address or
            not isinstance(local_node_address, str) or
            local_node_address == ''
        ) and Config.address_not_provided()
    ):
        raise exceptions.HttpError(
            message="No address provided."
        )

    if not Config.address_not_provided():
        my_node_address = local_node_address
    else:
        my_node_address = Config.ADDRESS

    local_node_name = local_node.get('name', None)

    if (
        (
            not local_node_name or
            not isinstance(local_node_name, str) or
            local_node_name == ''
        ) and Config.name_not_provided()
    ):
        raise exceptions.HttpError(
            message="No name provided."
        )

    if not Config.name_not_provided():
        my_node_name = local_node_name
    else:
        my_node_name = Config.NAME

    my_node = Node(
        id=None,
        name=my_node_name,
        server_address=my_node_address
    )

    external_node = json_body.get('external_node', None)

    if not external_node or not isinstance(external_node, dict):
        raise exceptions.HttpError(
            message="No external node address and name information provided."
        )

    external_node_address = external_node.get('server_address', None)

    if (
        not external_node_address or
        not isinstance(external_node_address, str) or
        external_node_address == ''
    ):
        raise exceptions.HttpError(
            message="No external node address provided."
        )

    external_node = json_body.get('external_node', None)

    if not external_node or not isinstance(external_node, dict):
        raise exceptions.HttpError(
            message="No external node address and name information provided."
        )

    external_node_name = external_node.get('name', None)

    if (
        not external_node_name or
        not isinstance(external_node_name, str) or
        external_node_name == ''
    ):
        raise exceptions.HttpError(
            message="No external node name provided."
        )

    new_node = Node(
        id=None,
        name=external_node_name,
        server_address=external_node_address
    )
    print(new_node)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(
        new_node.server_address + '/registry/',
        data = json.dumps(my_node.to_dict()),
        headers = headers
    )

    new_nodes = [Node(**data) for data in r.json()]

    for node in new_nodes:
        Storage.post_registry(node)

    new_nodes.append(my_node)
    return jsonify(new_nodes), 200
    # return jsonify([[node.to_dict() for node in new_nodes]]), 200


@app.route("/search", methods=['GET'])
def search_tweet():

    query_params = {}

    content = request.args.get('content', None)

    if content:
        query_params.update({'content': content})

    created_from = request.args.get('created_from', None)
    if created_from:
        query_params.update({'created_from': created_from})
        created_from = datetime.fromtimestamp(
            int(created_from)/1000
        )
    created_to = request.args.get('created_to', None)
    if created_to:
        query_params.update({'created_to': created_to})
        created_to = datetime.fromtimestamp(
            int(created_to)/1000
        )

    all_tweets = []
    all_nodes = request.args.get('all',False)
    if all_nodes:
        other_nodes = Storage.get_nodes()
        for node in other_nodes:
            try:
                node_tweets = [Tweet(**data) for data in requests.get(
                    node.server_address + '/search', query_params
                ).json()]

            except:
                node_tweets = []

            all_tweets.extend(node_tweets)

    tweets = Storage.search_tweet(
        content, created_from, created_to
    )

    all_tweets.extend(tweets)
    return jsonify([tweet.to_dict() for tweet in all_tweets]), 200

@app.route("/tweets/retweet", methods=['POST'])
def post_retweet():
    if not request.get_json():
        raise exceptions.HttpError(message="No info")

    name = request.get_json()['name']
    id = request.get_json()['id']


    post_retweet = Tweet(
        id=None,
        name=None,
        tweet=request.get_json()["tweet"],
        created_at=None,
        type = 'retweet'
    )


# if __name__ == "__main__":
#       Storage.create_db_table()
#       app.run(host='0.0.0.0')
