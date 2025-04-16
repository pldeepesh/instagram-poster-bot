import psycopg2
from psycopg2 import sql
from datetime import datetime
import json

def get_connection():
    # Connection creds
    file = open("creds.json",'rb')
    CONFIG = json.load(file)
    file.close()

    """Inserts APOD data into the PostgreSQL database."""
    # Database connection parameters
    conn_params = {
        'dbname': 'starry_post_daily',
        'user': CONFIG['postgres']['USER_NAME'],
        'password': CONFIG['postgres']['PASSWORD'],
        'host': CONFIG['postgres']['HOST'],
        'port': CONFIG['postgres']['PORT']
    }
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**conn_params)

    return conn

def insert_apod_data(data):
    conn = get_connection()
    cursor = conn.cursor()
    # SQL query for inserting data
    insert_query = sql.SQL("""
        INSERT INTO apod_responses (
                           date, 
                           title, 
                           explanation, 
                           url, 
                           media_type, 
                           copyright,
                           service_version,
                           hdurl, 
                           api_full_response, 
                           api_start_ts,
                           api_end_ts,
                           api_status_code,
                           created_at, 
                           updated_at,
                           tags
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id
    """)
    
    # Current timestamp
    current_timestamp = datetime.now()
    
    # Execute the insert query
    try:
        cursor.execute(insert_query, (
            data['date'], 
            data['title'], 
            data['explanation'], 
            data['url'], 
            data['media_type'], 
            data['copyright'],
            data['service_version'],
            data['hdurl'], 
            data['api_full_response'], 
            data['api_start_ts'],
            data['api_end_ts'],
            data['api_status_code'],
            current_timestamp,
            current_timestamp,
            data['tags']
        ))
        inserted_id= cursor.fetchone()[0]
        conn.commit()
        print("Data inserted successfully.")
        return inserted_id
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()



# apod_data = {'date':'2024-08-03',
# 'title':'Glory and Fog Bow',
# 'explanation':"On a road trip up Mount Uluda\u011f in Bursa province, Turkey these motorcyclists found themselves above low clouds and fog in late June. With the bright Sun directly behind them, the view down the side of the great mountain revealed a beautiful, atmospheric glory and fog bow. Known to some as the heiligenschein or the Specter of the Brocken, a glory can also sometimes be seen from airplanes or even high buildings. It often appears to be a dark giant surrounded by a bright halo. Of course the dark giant is just the shadow of the observer (90MB video) cast opposite the Sun. The clouds and fog are composed of very small water droplets, smaller than rain drops, that refract and reflect sunlight to create the glory's colorful halo and this more extensive fog bow.",
# 'url':'https://apod.nasa.gov/apod/image/2408/GloryFog_label.png',
# 'media_type':'image',
# 'copyright':"Cem \u00d6zkeser",
# 'service_version':'V1',
# 'hdurl':'https://apod.nasa.gov/apod/image/2408/GloryFog1.jpg',
# 'api_full_response':json.dumps('''{"copyright":"Cem \u00d6zkeser","date":"2024-08-03","explanation":"On a road trip up Mount Uluda\u011f in Bursa province, Turkey these motorcyclists found themselves above low clouds and fog in late June. With the bright Sun directly behind them, the view down the side of the great mountain revealed a beautiful, atmospheric glory and fog bow. Known to some as the heiligenschein or the Specter of the Brocken, a glory can also sometimes be seen from airplanes or even high buildings. It often appears to be a dark giant surrounded by a bright halo. Of course the dark giant is just the shadow of the observer (90MB video) cast opposite the Sun. The clouds and fog are composed of very small water droplets, smaller than rain drops, that refract and reflect sunlight to create the glory's colorful halo and this more extensive fog bow.","hdurl":"https://apod.nasa.gov/apod/image/2408/GloryFog1.jpg","media_type":"image","service_version":"v1","title":"Glory and Fog Bow","url":"https://apod.nasa.gov/apod/image/2408/GloryFog_label.png"}'''),
# 'api_start_ts':'2024-08-03',
# 'api_end_ts':'2024-08-03',
# 'api_status_code':200,
# 'tags':'astro, nasa, apod'}
# insert_apod_data(apod_data)

def insert_insta_posts(insta_posts_data):
    conn = get_connection()
    cursor = conn.cursor()

    # SQL query for inserting data
    insert_query = sql.SQL("""
        INSERT INTO insta_posts (
                           apod_responses_id,
                           posted_to_instagram,
                           insta_post_time,
                           reason,
                           created_at,
                           updated_at,
                           caption,
                           final_url,
                           tags
                           
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id
    """)
    # Current timestamp
    current_timestamp = datetime.now()
    
    # Execute the insert query
    try:
        cursor.execute(insert_query, (
            insta_posts_data['apod_responses_id'],
            insta_posts_data['posted_to_instagram'],
            insta_posts_data['insta_post_time'],
            insta_posts_data['reason'],
            current_timestamp,
            current_timestamp,
            insta_posts_data['caption'],
            insta_posts_data['final_url'],
            insta_posts_data['tags']
        ))
        inserted_id= cursor.fetchone()[0]
        conn.commit()
        print("Data inserted successfully.")
        return inserted_id
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# insta_posts_data = {
#                         'apod_responses_id':1,
#                         'posted_to_instagram':False,
#                         'insta_post_time':None,
#                         'reason':None,
#                         'final_url':None,
#                         'tags':None,
#                         'caption':None
#                     }

# insert_insta_posts(insta_posts_data)