from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded
import time
import pandas as pd

print('What is the file path?')
file = input()
print('What is the API key?')
apiKey = input()
print('What is the name of the column to geocode?')
toGeocode = input()
print('What do you what to name the  new file name?')
newFile = input()

# read in data frame
latlon = pd.read_csv(file)

geolocator = GoogleV3(api_key=apiKey)


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


latlon['location'] = latlon[toGeocode].apply(lambda x: geocode_me(x))
latlon['point'] = latlon['location'].apply(lambda loc: tuple(loc.point) if loc else None)
latlon[['Location_Lat', 'Location_Lon', 'altitude']] = pd.DataFrame(latlon['point'].tolist(), index=latlon.index)
latlon.to_csv(newFile)
