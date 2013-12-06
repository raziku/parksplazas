__author__ = 'eddiexie'

import time

def compute_stats():
    parks = get_all_parks()
    conn = pymongo.MongoClient(host='grande.rutgers.edu')
    time_window = 3600

    for park in parks:
        print park.get_name()
        current_time = int(time.time())
        previous = current_time - time_window
        cursor_read = conn['citybeat_production'][park.get_id()]

        photos = cursor_read.find({'data_type': 'photo',
                                   'created_time': {"$lt":str(current_time),
                                                    "$gt": str(previous)}})




