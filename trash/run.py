from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api
import json
import pymongo


app = Flask(__name__)
api = Api(app)


class Park(Resource):
    def get(self, park_id):
        park_id = str(park_id)
        conn = pymongo.MongoClient(host='grande.rutgers.edu')
        cursor_read = conn['parks_plazas'][park_id]

        latest_photos = [p for p in cursor_read.find({"datatype":"photo", }).limit(10)]
        latest_tweets = [t for t in cursor_read.find({"datatype":"tweet", }).limit(10)]

        trend = [t for t in cursor_read.find({'datatype':'trend'}).limit(1)][0]

        tweet_keywords = [t for t in cursor_read.find({'datatype':'tweet_keywords'}).limit(1)][0]['tweet_keywords']
        photo_keywords = [p for p in cursor_read.find({'datatype':'photo_keywords'}).limit(1)][0]['photo_keywords']

        conn.close()
        return {'photos': latest_photos,
                'tweets': latest_tweets,
                'trend': trend['trend'],
                'tweet_keywords': tweet_keywords,
                'photo_keywords': photo_keywords
                }


api.add_resource(Park,
    '/park/<string:park_id>', endpoint='park')

class Trending(Resource):
    def get(self):
        print 'in trending'
        conn = pymongo.MongoClient(host='grande.rutgers.edu')
        cursor_read = conn['parks_plazas']['most_trending']

        trending = [t['most_trending'] for t in cursor_read.find().limit(1)]
        return trending

api.add_resource(Trending,
    '/trending', endpoint='trending')





if __name__ == '__main__':
    app.run(debug=True)
