__author__ = 'eddiexie'



import shapely


from fiona import collection
from shapely.geometry import shape
from shapely.geometry import Point


from venue import Venue

def get_all_parks():
    parks = []
    ids = []

    with collection(
        "./gis_files/DPR_FunctionalParkland_001_LATLONG.shp", "r") as input:
        for n, p in enumerate(input):
            park_name = p['properties']['SIGNNAME']
            park_poly = shape(p['geometry'])
            my_venue = Venue(park_name, park_poly, p['properties']['GISPROPNUM'], p['properties'])
            ids.append(p['properties']['GISPROPNUM'])
            #print 'Park name: ', my_venue.get_name(), ' with poly ', my_venue.get_poly()
            # 40.7812, -73.9666 a point in central park
            #if Point(-73.9666, 40.7812).within(my_venue.get_poly()):
            #    print 'in ', my_venue.get_name()
            #my_poly =  shape(p['geometry'])
            #my_point = Point( 41,42   )
            #print my_point.within(my_poly)
            #print my_poly

            #print park_name
            parks.append(my_venue)
    print len(ids), len(set(ids))
    return parks

