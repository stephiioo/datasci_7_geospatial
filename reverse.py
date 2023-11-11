import requests
import urllib.parse
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = "AIzaSyDphlj0Sy2epGxctkr_qI5W15gha5nleDc"

# Sample Data
sample_data = {'X': [44.02010494, 45.31536792, 44.1120137],
               'Y': [-92.43931254, -96.44581588, -93.25109201]}

df = pd.DataFrame(sample_data)

df['GEO'] = df['X'].astype(str) + ',' + df['Y'].astype(str)

google_response = []

for index, row in df.iterrows():
    location_raw = row['GEO']
    location_clean = urllib.parse.quote(location_raw)

    reverse_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
    request_url = reverse_geocode_url + location_clean + '&key=' + API_KEY

    response = requests.get(request_url)
    response_dictionary = response.json()

    if 'results' in response_dictionary and response_dictionary['results']:
        address = response_dictionary['results'][0]['formatted_address']
        final = {'address': address, 'coordinates': location_raw}
        google_response.append(final)
        print(f'Finished with {location_raw}')
    else:
        print(f'No results found for {location_raw}')

df_add = pd.DataFrame(google_response)

df_add.to_csv('reverse_geocoding.csv', index=False)
