#reference https://www.w3schools.com/html/html5_audio.asp
#reference https://docs.genius.com/#search-h2
#reference https://github.com/jomart-gsu/csc4350-lect7-demo/blob/main/app.py
#reference https://github.com/jomart-gsu/csc4350-lect7-demo/blob/main/nyt.py
#reference https://www.youtube.com/watch?v=-5VSXXAQdnA
#reference https://www.youtube.com/watch?v=tybKOpPSsSE
import requests
import os
import random
from flask import Flask, render_template
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())

genius_token = os.getenv("GENIUS_TOKEN")
genius_url = "https://api.genius.com/search"



def get_song_data():
    spotify_url = "https://api.spotify.com/v1/artists/"
    authorization_url = "https://accounts.spotify.com/api/token"
    accessname = os.getenv("ID")
    accesskey = os.getenv("PASSWORD")
    auth_res = requests.post(
    authorization_url,{
    "grant_type":"client_credentials",
    "client_id" : accessname,
    "client_secret" : accesskey
    })
    auth_response_data = auth_res.json()
    access_token = auth_response_data["access_token"]
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    num = random.randint(0,2)
    favorite_artist = ["04gDigrS5kc9YWfZHwBETP","31TPClRtHm23RisEBtV3X7","06HL4z0CvFAxyc27GXpf02"]
    singledata = requests.get(spotify_url + favorite_artist[num] + "/top-tracks", headers=headers, params={'market': 'US'})
    songs = singledata.json()

    songtitles = songs['tracks'][num]['name']
    songartists = songs['tracks'][num]['artists'][0]['name']
    songimgs = songs['tracks'][num]['album']['images'][0]['url']
    songprevs = songs['tracks'][num]['preview_url']
    print(songtitles)
    print(songartists)
    print(songimgs)
    print(songprevs)
    
    params = {
        'q': songtitles,
        'access_token' : genius_token
    }
    response = requests.get(genius_url, params=params)
    data = response.json()
    songlyrics = data["response"]["hits"][0]["result"]["url"]
    print(songlyrics)
    return {
        "songtitles": songtitles,
        "songartists": songartists,
        "songimgs" : songimgs,
        "songprevs" : songprevs,
        "songlyrics": songlyrics
    }

