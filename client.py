import requests
import json

url = "http://import.sedamcvrkuta.com:8000/tweets/"

r = requests.post(
    url,
    json = json.dumps({'tweet': 'Hello world 1!'})
)

r = requests.post(
    url,
    json = json.dumps({'tweet': "Hello world 2!"})
)
r = requests.post(
    url,
    json = json.dumps({'tweet': "Hello world 3!"})
)

tweet_id = 1
r = requests.get("{}{}".format(url, tweet_id))
print("tweet ({}): ".format(tweet_id), r.text)

tweet_id = 2
r = requests.delete("{}{}".format(url, tweet_id))
