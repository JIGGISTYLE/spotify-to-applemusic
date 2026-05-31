from fastapi import FastAPI

# pyrefly: ignore [missing-import]
from fastapi.responses import RedirectResponse

import urllib.parse
from main import params
app=FastAPI()

@app.get("/")
def home():
    return {"message":"spotify to apple music"}

@app.get("/convert")
def request_auth(): # login
    url_part=urllib.parse.urlencode(params) # convert dictionary to querystring
    spotify_auth_url=f"https://accounts.spotify.com/authorize?{url_part}"
    return RedirectResponse(url=spotify_auth_url)


    