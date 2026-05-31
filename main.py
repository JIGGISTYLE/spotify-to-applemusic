from functions import Genrate_random_string

CLIENT_ID="13819ba30de24038a805408db081d31b"
CLIENT_SECRET="25ff69e60cc64bddb6e23121029a5b51"

# REQUEST USER AUTHERIZAION - https://developer.spotify.com/documentation/web-api/tutorials/code-flow

client_id=CLIENT_ID
response_type="code"
redirect_uri="http://127.0.0.1:8000/" # use uri not url
state=Genrate_random_string(16)
scope="playlist-read-private"


params = {"client_id":client_id, "response_type":response_type, "scope":scope, "state":state, "redirect_uri":redirect_uri}