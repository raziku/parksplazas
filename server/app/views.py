from flask import render_template
import json
from app import app
import pymongo
import time

#app = Flask(__name__)
#api = Api(app)



@app.route('/trending', methods = ['GET'])
def get_trending():
    conn = pymongo.MongoClient(host='grande.rutgers.edu')
    cursor_read = conn['parks_plazas']['most_trending']

    #park_id_list = [p for p in cursor_read.find().limit(1)][0]

    park_id_list = [p for p in cursor_read.find().sort("created_time", -1).limit(1)][0]

    park_id_list = park_id_list['most_trending']

    print len(park_id_list)

    """
    parks = []
    for park in park_id_list[:3]:
        print 'working on ', park
        parks.append(get_single_park_dic(park))
    """
    return render_template(
        "trending.html", parks = park_id_list
    )





def get_single_park_dic(park_id):
    park_id = str(park_id)
    conn = pymongo.MongoClient(host='grande.rutgers.edu')
    cursor_read = conn['parks_plazas'][park_id]

    latest_photos = [p for p in cursor_read.find({"datatype": "photo", }).limit(10)]
    latest_tweets = [t for t in cursor_read.find({"datatype": "tweet", }).limit(10)]

    current_time = int(time.time())
    tweet_count = cursor_read.find({"datatype": "tweet",
                                     'created_time': {'$lt': str(current_time),
                                                      '$gt': str(current_time - 24*3600) }}).count()
    photo_count = cursor_read.find({"datatype": "photo",
                                    'created_time': {'$lt': str(current_time),
                                                     '$gt': str(current_time - 24*3600) }}).count()

    trend = [t for t in cursor_read.find({'datatype': 'trend'}).limit(1)][0]

    tweet_keywords = [t for t in cursor_read.find({'datatype': 'tweet_keywords'}).limit(1)][0]['tweet_keywords']
    photo_keywords = [p for p in cursor_read.find({'datatype': 'photo_keywords'}).limit(1)][0]['photo_keywords']

    conn.close()
    park_dic={'photos': latest_photos,
              'tweets': latest_tweets,
              'trend': trend['trend'],
              'tweet_keywords': tweet_keywords,
              'photo_keywords': photo_keywords,
              'tweet_count': tweet_count,
              'photo_count': photo_count
    }
    return park_dic

@app.route('/park/<string:park_id>', methods = ['GET', 'POST'])
def get_park(park_id):
    print 'IN get'
    park_dic = get_single_park_dic(park_id)
    return render_template("park.html",
                           park_dic = park_dic)



#if __name__ == '__main__':
#    app.run(debug=True)
