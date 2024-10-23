import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/spotify_artist_tracks_2020.csv')
    return df

# Load the data into the app
df = load_data()

# App Title
st.title("Spotify Songs Data: Statistical Analysis (2020)")

# Display the raw data
st.header("Raw Data")
st.write(df.head())

# Show basic statistics
st.header("Basic Statistics for Numerical Columns")
st.write(df.describe(include=np.number).T)