import geopy.distance

def getMeterDistanceBetweenTwoLocations(lat1, long1, lat2, long2):
    coords_1 = (lat1, long1)
    coords_2 = (lat2, long2)

    return geopy.distance.distance(coords_1, coords_2).m
