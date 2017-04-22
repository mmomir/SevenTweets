from storage import Storage

def test():
    return True

def test_get_tweets():
    Storage._tweets.clear()
    Storage._tweets.append(12)
    assert Storage.get_tweets() == [12]
