# for yt side , router are used when there are multiple endpoints 

import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from fastapi import APIRouter ,  Query, HTTPException , Header
# pyrefly: ignore [missing-import]
from fastapi.responses import RedirectResponse
import urllib.parse

import requests

import time

load_dotenv()
router=APIRouter()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8000/youtube/callback"


@router.get("/auth")
def youtube_auth():
    # 1. Define the parameters for the Google OAuth 2.0 request
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        # Requesting YouTube scope to allow playlist management
        "scope": "https://www.googleapis.com/auth/youtube",
        "access_type": "offline",  # set to 'offline'
        "prompt": "consent"        # Forces the consent screen to show
    }
    
    # 2. Build the authorization URL
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)   # convert dictionary to querystring
    
    # 3. Redirect the user to Google
    return RedirectResponse(url=auth_url)

#request_youtube_access_token
@router.get("/callback")
def youtube_callback(code: str = Query(...)):
    # 1. Exchange the authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI
    }
    
    response = requests.post(token_url, data=payload)
    token_data = response.json()
    
    if "error" in token_data:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {token_data['error']}")
    
    # 2. Extract tokens
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    
    # return {"message": "Successfully connected to YouTube!","access_token": access_token}
    streamlit_url = f"http://localhost:8501/?yt_access_token={access_token}"
    return RedirectResponse(url=streamlit_url)

@router.post("/create_playlist")
def create_playlist(
    playlist_name: str, 
    video_ids: list[str], 
    authorization: str = Header(...)
):
    """
    1. Creates a new private playlist on the user's YouTube channel.
    2. Populates it with the provided list of video_ids.
    """
    # URL and Headers for YouTube API
    headers = {"Authorization": authorization, "Content-Type": "application/json"}
    
    # 1. Create the empty playlist
    playlist_url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status"
    playlist_body = {
        "snippet": {"title": playlist_name},
        "status": {"privacyStatus": "private"}
    }
    
    response = requests.post(playlist_url, headers=headers, json=playlist_body)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, 
            detail=f"Failed to create playlist: {response.text}"
        )
    
    playlist_id = response.json().get("id")

    # 2. Add videos to the playlist (using loop)
    item_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
    for vid in video_ids:
        item_body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video", 
                    "videoId": vid
                }
            }
        }
        
        # Add a small delay if you have a massive playlist to stay under rate limits
        requests.post(item_url, headers=headers, json=item_body)
        time.sleep(0.5) 

    return {
        "message": "Playlist created and populated successfully!", 
        "playlist_id": playlist_id
    }