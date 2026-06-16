import random
import string
import urllib.parse
import requests
from fastapi import HTTPException
def Genrate_random_string(length):
    charachters = string.ascii_letters + string.digits
    return "".join(random.choices(charachters,k=length))



def get_playlist_from_spotify(access_token,playlist_id):

    url=f"https://api.spotify.com/v1/playlists/{playlist_id}"
    header={"Authorization":f"Bearer {access_token}"}
    try:
        response=requests.get(url,headers=header)
        if response.status_code==200:
            return response.json()
        else:
            raise HTTPException (status_code=response.status_code, detail=f"Spotify API Error: {response.text}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")

def get_playlist_id(playlist_link):
    # playlist_link=input("enter link") #https://open.spotify.com/playlist/3QoWh6CX1qHA4HH0TqEuCw?si=cVOFpwANSoWapZbr5zekVQ
    path = urllib.parse.urlparse(playlist_link).path # to get only "/playlist/3QoWh6CX1qHA4HH0TqEuCw"
    playlist_id = path.split("/playlist/")[1]
    return playlist_id


    