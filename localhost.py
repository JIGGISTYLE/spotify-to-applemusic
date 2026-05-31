from fastapi import FastAPI,Query,HTTPException

# pyrefly: ignore [missing-import]
from fastapi.responses import RedirectResponse

import urllib.parse
from main import params,state,CLIENT_ID,CLIENT_SECRET,redirect_uri

import base64
import requests

app=FastAPI()

@app.get("/")
def home():
    return {"message":"spotify to apple music"}

@app.get("/convert")
def request_auth(): # login
    url_part=urllib.parse.urlencode(params) # convert dictionary to querystring
    spotify_auth_url=f"https://accounts.spotify.com/authorize?{url_part}"
    return RedirectResponse(url=spotify_auth_url)


original_state=state

@app.get("/callback")
def request_access_token():
    code: str = Query(None)
    state: str = Query(None)
    error: str = Query(None)

    if error :
        raise HTTPException (status_code=400,detail=f"spotify error {error}")
    if state!=original_state or (not state) :
        raise HTTPException (status_code=400 , detail ="state_mismatch")
    if not code:
        raise HTTPException (status_code=400 , detail="authcode not found")

    # preparing post request to token endpoint

    #header
    credential={CLIENT_ID:CLIENT_SECRET}
    base64_credential= base64.b64(credential.encode("utf-8")).decode("utf-8")
    header={"Authorization":f"basic {base64_credential}", "content-type":"application/x-www-form-urlencoded"}
    
    #body
    body={"grant_type":"authorization_code", "code":code ,"redirect_uri":redirect_uri}

    # posting
    token_url='https://accounts.spotify.com/api/token'

    try:
        response=requests.post(url=token_url,headers=header,data=body)
        response_data=response.json


        if response.status_code!=200 :
            return { "error":"faild to exchange token", "spotify detail":response_data}

        access_token = response_data.get("access_token") 
        token_type = response_data.get("token_type")
        scope = response_data.get("scope")
        expires_in = response_data.get("expires_in")
        refresh_token = response_data.get("refresh_token")

        return {"status":"authentiction succesfull","access_token":access_token,"token_type":token_type, "scope":scope, 
        "expires_in":expires_in, "refresh_token":refresh_token}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"netowk error {str(e)}")