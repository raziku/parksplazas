from flask import Flask, request
from flask.ext.restful import Resource, Api


import pymongo

app = Flask(__name__)
api = Api(app)

todos = {}


class Park(Resource):
    def get(self, park_id):
        park_id = str(park_id)
        conn = pymongo.MongoClient(host='grande.rutgers.edu')
        cursor_read_photos = conn['parks_plazas']['single_day']
        res = cursor_read_photos.find_one({'_id': park_id})
        conn.close()
        return res


api.add_resource(Park,
    '/park/<string:park_id>', endpoint='park')

if __name__ == '__main__':
    app.run(debug=True)
