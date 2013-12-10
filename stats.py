__author__ = 'eddiexie'

import time
import pymongo
from open_gis import get_all_parks
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def extract_topK_words(text, K):
    vectorizer = CountVectorizer(stop_words='english', min_df=0.01, max_df=0.8)
    try:
        X = vectorizer.fit_transform([text]).todense()
    except:
        return []
    index = np.argsort(X[0, :].tolist()[0])[::-1][:K]
    words = []
    for i in index:
        words.append(vectorizer.get_feature_names()[i])
    return words


def compute_stats():
    parks = get_all_parks()
    conn = pymongo.MongoClient(host='grande.rutgers.edu')
    time_window = 3600*24
    n_days_average = 7
    n_most_trending = 100
    
    n_photos = 10
    n_tweets = 10

    trending_list = []
    print 'In program'
    current_time = int(time.time())
    previous = current_time - time_window

    for park in parks:
        print current_time, previous, park.get_name(), park.get_id()
        cursor_read = conn['parks_plazas'][park.get_id()]
        #cursor_read = conn['parks_plazas']['M010']

        photos = [p for p in cursor_read.find({'datatype': 'photo',
                             'created_time': {"$lt":str(current_time),"$gt": str(previous)}})]
        tweets = [t for t in cursor_read.find({'datatype': 'tweet',
                                   'created_time': {"$lt":str(current_time),
                                                    "$gt": str(previous)}})]

        photo_text = " ".join([photo['caption']['text'] for photo in photos
                               if 'caption' in photo and
                                  photo['caption'] is not None and
                                  'text' in photo['caption'] and
                                  photo['caption']['text'] is not None])
        tweet_text = " ".join([tweet['text'] for tweet in tweets])

        photo_keywords = extract_topK_words(photo_text, 20)
        tweet_keywords = extract_topK_words(tweet_text, 20)

        cnt_by_day = [0]*n_days_average

        for day in range(n_days_average):
            end_time = current_time - day*24*3600
            start_time = current_time - (day+1)*24*3600
            cnt_by_day[day] = cursor_read.find({'datatype':'photo', 'created_time': {'$lt': str(end_time),
                                                                                      '$gt': str(start_time)}}).count()

            cnt_by_day[day] += cursor_read.find({'datatype':'tweet', 'created_time': {'$lt': str(end_time),
                                                                                      '$gt': str(start_time)}}).count()

        if sum(cnt_by_day[1:]) <= 0:
            trend = None
        else:
            avg = np.average(cnt_by_day[1:])
            trend = cnt_by_day[0]*1.0/avg

        if cnt_by_day[0] >= 30:
            trending_list.append([trend, cnt_by_day[0], photo_keywords, tweet_keywords, park.get_name(), photos[:n_photos], tweets[:n_tweets]])

        cursor_save = conn['parks_plazas'][park.get_id()]
        #cursor_save = conn['parks_plazas']['M010']

        cursor_save.save({'datatype': 'tweet_keywords',
                          'created_time': str(current_time),
                          'tweet_keywords':tweet_keywords})
        cursor_save.save({'datatype': 'photo_keywords',
                          'created_time': str(current_time),
                          'photo_keywords':photo_keywords})

        cursor_save.save({'datatype': 'trend',
                          'created_time': str(current_time),
                          'trend': trend})

    print 'start trending...'

    most_trending = []
    
    for n, idx in enumerate(sorted(range(len(trending_list)), key = lambda x: trending_list[x][0], reverse=True)[:n_most_trending]):
    #for n, idx in enumerate(np.argsort(trending_list)[::-1][:n_most_trending]):
        #most_trending.append(parks[idx].get_id())
        print idx
        #most_trending.append( trending_list[idx] )
        
        most_trending.append(
                {
                'trend': trending_list[idx][0], 
                'n_tweets_and_photos': trending_list[idx][1],
                'photo_keywords': trending_list[idx][2],
                'tweet_keywords': trending_list[idx][3],
                'park_name': trending_list[idx][4], 
                'photos': trending_list[idx][5],
                'tweets': trending_list[idx][6],
                }
                )
    cursor_save = conn['parks_plazas']['most_trending']
    cursor_save.insert({'datatype': 'most_trending', 'most_trending': most_trending, 'created_time': str(current_time)})
    conn.close()
    print 'Done'

compute_stats()
