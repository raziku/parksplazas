__author__ = 'eddiexie'



import shapely


#from fiona import collection
from shapely.geometry import shape
from shapely.geometry import Point

from shapely.geometry import Polygon

import shapefile


from venue import Venue

def get_all_parks():
    parks = []
    ids = []

    sf = shapefile.Reader("./gis_files/DPR_FunctionalParkland_001_LATLONG.shp")

    for n, record in enumerate(sf.iterRecords()):
        park_name = record[1]
        id = record[0]

        points = sf.shape(n).points
        park_poly = Polygon(points)

        my_venue = Venue(park_name, park_poly, id)
        parks.append(my_venue)
        """
        if park_name.lower().find("central")!=-1:
            print 'ha park ', park_name
            if Point(-73.9666, 40.7812).within(my_venue.get_poly()):
                print 'in ', my_venue.get_name()
            #my_poly =  shape(p['geometry'])
            #my_point = Point( 41,42   )
            #print my_point.within(my_poly)
            #print my_poly
        """



    """
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
    """

    return parks

"""

import shapefile
sf = shapefile.Reader("./gis_files/DPR_FunctionalParkland_001_LATLONG.shp")
for n,t in enumerate(sf.iterRecords()):
    print  t, sf.shape(n).points
"""


#for p in get_all_parks():
#    print p.get_properties()


