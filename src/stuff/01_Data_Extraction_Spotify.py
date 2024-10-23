# Obtaining Access Token
"""
The access token is essential for making authorized requests to the Spotify API. 
We obtain the access token by sending a POST request to the Spotify token endpoint with our 
client credentials encoded in Base64. This token serves as temporary authorization, 
allowing our application to fetch music data from Spotify.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import base64
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Access the client ID and client secret from the environment
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8888/callback"

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# List of artist names
artists = ['Drake', 'Taylor Swift', 'Bad Bunny', 'Ed Sheeran', 'The Weeknd']

# Function to get track details and audio features for a given artist, filtered by year 2020
def get_tracks_for_artist(artist_name):
    results = sp.search(q='artist:' + artist_name, type='track', limit=50)
    tracks = []
    
    for track in results['tracks']['items']:
        # Check the release date of the album/track and filter for 2020
        release_date = track['album']['release_date']
        release_year = int(release_date.split('-')[0])  # Extract the year from release date
        
        if release_year == 2020:  # Only include tracks from 2020
            track_id = track['id']
            track_name = track['name']
            album_name = track['album']['name']
            popularity = track['popularity']
            explicit = track['explicit']
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            
            # Get audio features
            audio_features = sp.audio_features([track_id])[0]
            if audio_features:
                track_info = {
                    'track_id': track_id,
                    'track_name': track_name,
                    'album_name': album_name,
                    'artists': artist_names,
                    'popularity': popularity,
                    'duration_ms': track['duration_ms'],
                    'explicit': explicit,
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'key': audio_features['key'],
                    'loudness': audio_features['loudness'],
                    'mode': audio_features['mode'],
                    'speechiness': audio_features['speechiness'],
                    'acousticness': audio_features['acousticness'],
                    'instrumentalness': audio_features['instrumentalness'],
                    'liveness': audio_features['liveness'],
                    'valence': audio_features['valence'],
                    'tempo': audio_features['tempo'],
                    'time_signature': audio_features['time_signature'],
                    'track_genre': 'Unknown'  # Spotify API doesn't return genre in track object; you might need to retrieve genres separately.
                }
                tracks.append(track_info)
    
    return tracks

# Collect track data for all artists, filtered by year 2020
all_tracks = []
for artist in artists:
    artist_tracks = get_tracks_for_artist(artist)
    all_tracks.extend(artist_tracks)

# Create a pandas DataFrame
df = pd.DataFrame(all_tracks)

# Save the DataFrame to a CSV file
df.to_csv('data/spotify_artist_tracks_2020.csv', index=False)

print('Data saved to spotify_artist_tracks_2020.csv')






