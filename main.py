import os
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import spotipy

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    st.error("Please make sure all environment variables are set in the .env file.")
else:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="user-top-read"
        )
    )

    st.set_page_config(page_title="Spotify Dashboard", page_icon=":musical_note:")
    st.title("Analysis for your Top Songs")
    st.write("Discover insights about your Spotify listening habits.")

    top_tracks = sp.current_user_top_tracks(limit=10, time_range="short_term")
    track_ids = [track["id"] for track in top_tracks["items"]]
    audio_features = sp.audio_features(track_ids)

    df = pd.DataFrame(audio_features)
    df["track_name"] = [track["name"] for track in top_tracks["items"]]
    df = df[["track_name", "danceability", "energy", "valence"]]
    df.set_index("track_name", inplace=True)

    st.subheader("Audio Features for Top Tracks")
    st.bar_chart(df, height=500)
