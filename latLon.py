from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded
import time
import pandas as pd

dataFile = 'a_file_path'

# read in data frame
nullLoc = pd.read_csv(dataFile)

geolocator = Nominatim(user_agent="FB")

def geocode_me(location):
    time.sleep(1.1)
    try:
        return geolocator.geocode(location)
    except (GeocoderTimedOut, GeocoderQuotaExceeded) as e:
        if GeocoderQuotaExceeded:
            print(e)
        else:
            print(f'Location not found: {e}')
            return None

nullLoc['location'] = nullLoc['address'].apply(lambda x: geocode_me(x))
nullLoc['point'] = nullLoc['location'].apply(lambda loc: tuple(loc.point) if loc else None)
nullLoc[['Location_Lat', 'Location_Lon', 'altitude']] = pd.DataFrame(nullLoc['point'].tolist(), index=nullLoc.index)
nullLoc.to_csv('/home/hunter/Food Bank Data/agency_data/latlonfix.csv')