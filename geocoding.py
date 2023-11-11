import requests
import pandas as pd
import urllib.parse
from dotenv import load_dotenv
import json
import os

load_dotenv()

API = "AIzaSyDphlj0Sy2epGxctkr_qI5W15gha5nleDc"

df = pd.read_csv("/Users/stephanieogbebor/Desktop/geospatial data/datasci_7_geospatial/assignment7_slim_hospital_addresses.csv")

df['GEO'] = df['ADDRESS'] + ' ' + df['CITY'] + ' ' + df['STATE']

# Loading a sample
df_s = df.sample(n=100)

google_response = []

for index, row in df_s.iterrows():
    address = row['GEO']
    search = 'https://maps.googleapis.com/maps/api/geocode/json?address='

    location_raw = address
    location_clean = urllib.parse.quote(location_raw)

    url_request_part1 = search + location_clean + '&key=' + API
    url_request_part1

    response = requests.get(url_request_part1)
    response_dictionary = response.json()

    # Check if there are any results before accessing the first result
    if 'results' in response_dictionary and response_dictionary['results']:
        lat_long = response_dictionary['results'][0]['geometry']['location']
        lat_response = lat_long['lat']
        lng_response = lat_long['lng']

        final = {'310 EAST 14TH STREET NEW YORK NY': address, 'lat': lat_response, 'lon': lng_response}
        google_response.append(final)
        print(f'....finished with {address}')
    else:
        print(f'No results found for {address}')

df_geo = pd.DataFrame(google_response)

df_geo.to_csv('geocoding.csv')

