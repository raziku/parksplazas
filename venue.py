__author__ = 'eddiexie'


class Venue():
    def __init__(self, name, poly, id, properties = None):
        # each venue is defined to be the ploy area it takes, and its name
        self.name = name
        self.poly = poly
        self.id = id
        self.properties = properties

        self.photos = []
        self.tweets = []

        self.photo_keywords = []
        self.tweet_keywords = []

    def get_id(self):
        return self.id

    def get_photos(self):
        return self.photos

    def get_tweets(self):
        return self.tweets

    def get_name(self):
        return self.name

    def get_poly(self):
        return self.poly

    def get_properties(self):
        return self.properties

    def get_photo_keywords(self):
        return self.photo_keywords

    def get_tweet_keywords(self):
        return self.tweet_keywords

    def add_photo(self, photo):
        self.photos.append(photo)

    def add_tweet(self, tweet):
        self.tweets.append(tweet)

    def add_photo_keywords(self, keywords):
        self.photo_keywords = keywords

    def add_tweet_keywords(self, keywords):
        self.tweet_keywords = keywords