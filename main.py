from functions import Genrate_random_string
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")

# REQUEST USER AUTHERIZAION - https://developer.spotify.com/documentation/web-api/tutorials/code-flow

client_id=CLIENT_ID
response_type="code"
redirect_uri="http://127.0.0.1:8000/callback" # use uri not url
state=Genrate_random_string(16)
scope="playlist-read-private"


params = {"client_id":client_id, "response_type":response_type, "scope":scope, "state":state, "redirect_uri":redirect_uri}
print(params)