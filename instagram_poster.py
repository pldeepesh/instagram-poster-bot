import requests
from instabot import Bot
import json
from db_connections import get_connection,insert_insta_posts
import pandas as pd
from datetime import datetime
import os

def get_apod_data(apod_data_id):
    conn = get_connection()
    sql = f'''select * from apod_responses where id = {apod_data_id}'''
    
    apod_data = pd.read_sql_query(sql,conn)

    apod_data = json.loads(apod_data.to_json(orient = 'records'))
    apod_data = apod_data[0]

    conn.close()

    return apod_data

def delete_cookies():
    if os.path.exists("config/starrypostdaily_uuid_and_cookie.json"):
        os.remove("config/starrypostdaily_uuid_and_cookie.json")
        print("deleted cookies.json")


def post_to_instagram(apod_data_id,debug=False):

    file = open("creds.json",'rb')
    CONFIG = json.load(file)
    file.close()

    # Constants
    INSTAGRAM_USERNAME = CONFIG['instagram']['USER_NAME']
    INSTAGRAM_PASSWORD = CONFIG['instagram']['PASSWORD']

    # Initialize the Instagram bot
    delete_cookies()
    if debug==False:
        bot = Bot()
        bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)

    apod_data = get_apod_data(apod_data_id)

    response_text = {
                        'apod_responses_id':apod_data_id,
                        'posted_to_instagram':False,
                        'insta_post_time':None,
                        'reason':None,
                        'final_url':None,
                        'tags':apod_data['tags'],
                        'caption':None
                    }


    

    """ Posts an image to Instagram if it meets the criteria """
    if apod_data['media_type'] == 'image':
        if 'hdurl' in apod_data.keys():
            image_url = apod_data['hdurl']
            response_text['final_url'] = apod_data['hdurl']
        else:
            image_url = apod_data['url']
            response_text['final_url'] = apod_data['url']
        caption = apod_data.get('explanation', '')
        if 'copyright' in apod_data:
            if apod_data['copyright']==None:
                pass
            else:
                caption += f"\nCopyright: {apod_data['copyright']}"
        
        response_text['caption'] = caption

        hashtags = ''.join(["#"+x+" " for x in apod_data['tags'].split(',')])

        caption += f"\n"+hashtags

        # Download the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            filename = 'temp.jpg'
            with open(filename, 'wb') as img_file:
                img_file.write(img_response.content)

            # Post the image
            if debug==False:
                bot.upload_photo(filename, caption=caption)
            response_text['insta_post_time'] = datetime.now()
            response_text['posted_to_instagram'] = True
            insta_posts_id = insert_insta_posts(response_text)
            print("success fully posted to insta")
            return insta_posts_id
    else:
        response_text['reason'] = apod_data['media_type']
        insta_posts_id = insert_insta_posts(response_text)
        return insta_posts_id