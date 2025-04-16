from apod import get_apod_data
from instagram_poster import post_to_instagram


apod_id = get_apod_data()
print("data pulled successfully from APOD API - ID - ",apod_id)
if apod_id:
    print(post_to_instagram(apod_id,debug=False))