# pyrefly: ignore [missing-import]
import streamlit as st
from functions import get_playlist_from_spotify

backend_url="http://127.0.0.1:8000"
st.title("convert your spotify playliist")
link = st.text_input("paste your link here")

# check if any active session
if "authenticated" not in st.session.authenticated:
    st.session.authenticated=False


