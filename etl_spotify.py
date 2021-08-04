

import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

USER_ID = "gerardo.mayel"
TOKEN = "BQDXzT_jchmwTpSiZU0NBp_qxyT9dY9kp-EU9wfnBfL4jL7MEwRbSeEHZGqhIalSmtXvVeusjKkjMiFX2huOBMghbuQmkZpJJlVBpbGOiOMy6kRGVwmTLX5_AWr4Nq-ktcU2Ql4GZbCngs7nHXt15XDa"




def run():
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()
    
    song_names = []
    artist_names = []
    played_at_list = []
    timestapms = []
    
    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestapms.append(song["played_at"][0:10])
    
    song_dict = {
        'song_name' : song_names,
        'artist_name' : artist_names,
        'played_at' : played_at_list,
        'timestamp' : timestapms   
    }
    
    song_df = pd.DataFrame(song_dict, columns = ['song_name', 'artist_name', 'played_at', 'timestamp'])
    
    print(song_df)

if __name__ == "__main__":
    run()


