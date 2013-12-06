__author__ = 'eddiexie'

from open_gis import get_all_parks
import pymongo
import copy
from shapely.geometry import Point
from sklearn.feature_extraction.text import CountVectorizer
import time


def store_into_db(parks, data, data_type = 'photo'):
    taken = [0]*len(data)
    conn = pymongo.MongoClient(host='grande.rutgers.edu')
    for park in parks:
        print 'Processing for Park ', park.get_name(), park.get_id()
        cursor_store = conn['parks_plazas'][park.get_id()]
        cursor_store.ensure_index([('created_time', pymongo.ASCENDING), ('data_type', pymongo.ASCENDING)])
        for n, data_point in enumerate(data):
            if Point(data_point['location']['longitude'] , data_point['location']['latitude']).within(park.get_poly()):
                data_point['datatype'] = data_type
                data_point['_id'] = data_point['id']
                cursor_store.save(data_point)
                taken[n] = 1
        new_all_data = []
        for i in range(len(data)):
            if taken[i] == 0:
                new_all_data.append(data[i])
        data = new_all_data
        taken = [0]*len(data)


def transfer(start, end):
    # for each park, compute top keywords

    parks = get_all_parks()

    conn = pymongo.MongoClient(host='grande.rutgers.edu')
    cursor_read_photos = conn['citybeat_production']['photos']
    cursor_read_tweets = conn['citybeat_production']['tweets']
    print start, end
    condition = {'created_time':{'$lt': end, '$gt':start}}
    print 'fetching data...'
    all_photos = [photo for photo in cursor_read_photos.find(condition)]
    all_tweets = [tweet for tweet in cursor_read_tweets.find(condition)]
    print len(all_photos)
    print len(all_tweets)
    print 'fetching data done'


    store_into_db(parks, all_photos, 'photo')
    store_into_db(parks, all_tweets, 'tweet')


def run(days = 0):
    transfer(str(int(time.time() - days*24*3600)), str(int(time.time())) )


run(days = 7)