from storage import Storage


def test():
    return True

def test_get_tweets():
    Storage._tweets.clear()
    Storage._tweets.append(12)
    assert Storage.get_tweets() == [12]

def test_get_tweet():
    Storage._tweets.clear()
    Storage._tweets.append({"id": 1,"name": "Milos", "tweet":"Test"})
    assert Storage.get_tweet(1) == {"id": 1,"name": "Milos", "tweet":"Test"}

def test_post_tweet():
    Storage._tweets.clear()
    Storage.post_tweet("Test")
    assert Storage._tweets == [{"id": 1,"name": "Milos", "tweet":"Test"}]

def test_del_tweet():
    Storage._tweets.clear()
    Storage._tweets.append({"id": 1, "name": "Milos", "tweet":"Test"})
    Storage.del_tweet(1)
    assert Storage._tweets == []
