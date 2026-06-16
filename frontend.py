import streamlit as st
import requests
from functions import get_playlist_from_spotify, get_playlist_id
backend_url = "http://127.0.0.1:8000"

st.title("Convert Your Spotify Playlist")

# Check the URL for an access token returned by the FastAPI backend
if "access_token" in st.query_params:
    st.session_state.authenticated = True
    st.session_state.access_token = st.query_params["access_token"]
    st.query_params.clear() # Clear the all other URL parameters for a cleaner look

# Safely initialize the session state dictionary
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Display UI based on the user's authentication status
if not st.session_state.authenticated:
    st.write("Please connect your Spotify account to proceed.")
    
    # Render an HTML link to safely redirect the user's browser to the backend login route
    login_html = f'''
    <a href="{backend_url}/convert" target="_self">
        <button style="background-color:#1DB954; color:white; border:none; padding:10px 20px; border-radius:20px; cursor:pointer; font-weight:bold;">
            Connect Spotify
        </button>
    </a>
    '''
    st.markdown(login_html, unsafe_allow_html=True)

else:
    st.success("Spotify account connected successfully!")
    
    link = st.text_input("Paste your Spotify playlist link here:")
    
    if st.button("Convert Playlist"):
        if link:
            st.write("Processing your playlist...")
            playlist_id = get_playlist_id(link)
            data = get_playlist_from_spotify(st.session_state.access_token, playlist_id)
            st.write(data)
        else:
            st.warning("Please enter a valid playlist link.")