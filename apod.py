import requests
import json
from db_connections import insert_apod_data
from datetime import datetime
from hashtag_generator import generate_hashtags

def get_apod_data():
    file = open("creds.json",'rb')
    CONFIG = json.load(file)
    file.close()

    # Constants
    API_KEY = CONFIG['nasa']['API_KEY']
    NASA_APOD_URL = 'https://api.nasa.gov/planetary/apod'

    """ Fetches the APOD data from NASA's API """
    params = {'api_key': API_KEY}
    api_start_ts = datetime.now()
    response = requests.get(NASA_APOD_URL, params=params)
    api_end_ts = datetime.now()

    if response.status_code == 200:        
        apod_data = response.json()
        apod_data['api_full_response'] = json.dumps(apod_data)
        apod_data['api_start_ts'] = api_start_ts
        apod_data['api_end_ts'] = api_end_ts
        apod_data['api_status_code'] = response.status_code
        apod_data['tags'] = generate_hashtags(apod_data['explanation'])
        
        if 'copyright' not in apod_data.keys():
            apod_data['copyright'] = None
        apod_data_id = insert_apod_data(apod_data)
        return apod_data_id
    return None
