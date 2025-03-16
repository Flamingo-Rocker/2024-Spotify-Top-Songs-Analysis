#app.py
#importing the necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#loading the dataset
spotify_data = pd.read_csv(
    r"C:\Users\sethc\github_projects\2024-Spotify-Top-Songs-Analysis\Most Streamed Spotify Songs 2024.csv", 
    encoding='ISO-8859-1'
)

# Cleaning up the column names
spotify_data.columns = (
    spotify_data.columns.str.strip() #remove lead/trailing spaces
    .str.lower() #convert to lowercase
    .str.replace(r"[^\w\s]", "", regex=True)  # Remove special characters
    .str.replace(r"\s+", "_", regex=True) #convert to snake case
)

# Convert all_time_rank to integer
spotify_data['spotify_streams'] = spotify_data['spotify_streams'].str.replace(',', '').astype('Int64')
spotify_data['spotify_playlist_reach'] = spotify_data['spotify_playlist_reach'].str.replace(',', '').astype('Int64')
spotify_data['tiktok_posts'] = spotify_data['tiktok_posts'].str.replace(',', '').astype('Int64')

# Replacing missing values with 0
spotify_data = spotify_data.replace(" ", pd.NA)
spotify_data = spotify_data.replace("", pd.NA)
spotify_data = spotify_data.fillna(0)

# print(spotify_data.columns)

# Remove extraneous columns
spotify_data = spotify_data.drop(
    columns=['spotify_playlist_count',
             'spotify_popularity',
             'tiktok_likes',
             'tiktok_views',
             'youtube_views',
             'youtube_likes',
             'youtube_playlist_reach',
             'apple_music_playlist_count',
             'airplay_spins',
             'siriusxm_spins',
             'deezer_playlist_count',
             'deezer_playlist_reach',
             'amazon_playlist_count',
             'pandora_streams',
             'pandora_track_stations',
             'soundcloud_streams',
             'shazam_counts',
             'tidal_popularity',
             'explicit_track']
)

#Create release_year column
spotify_data['release_date'] = pd.to_datetime(spotify_data['release_date'])
spotify_data['release_year'] = spotify_data['release_date'].dt.year

# Create streamlit header
st.header("2024 Spotify Top Songs Analysis")

# Create streamlit slider and supporting dataframe for histogram
min_year = int(spotify_data['release_year'].min())
max_year = int(spotify_data['release_year'].max())

year_range = st.slider(
    'Select Release Year Range',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_histodata = spotify_data[
    (spotify_data['release_year'] >= year_range[0]) &
    (spotify_data['release_year'] <= year_range[1]) 
]

# Create plotly express histogram showing distribution of most streamed songs in 2024 by release year]
fig = px.histogram(
    filtered_histodata,
    x='release_year',
    title='Distribution of 2024 Spotify Most Streamed Songs by Release Year',
    labels={'release_year': 'Release Year', 'count': 'Number of Songs'},
    opacity=0.8,
    nbins=35,
    template='plotly_dark'
)

fig.update_layout(
    yaxis_title='Number of Songs',
    bargap=0.1
)
st.plotly_chart(fig)

# Create streamlit checkboxes for removing outlier x-variables
filter_playlist_reach = st.checkbox('Show only songs with Spotify Playlist Reach < 125000000', value=False)

# Create filter conditions for scat1
filtered_scat1 = spotify_data.copy()
if filter_playlist_reach:
    filtered_scat1 = filtered_scat1[filtered_scat1['spotify_playlist_reach'] < 125000000]

# Create scatter plot 1
scat1 = px.scatter(
    filtered_scat1,
    x='spotify_playlist_reach',
    y='spotify_streams',
    labels={'spotify_playlist_reach': 'Spotify Playlist Reach', 'spotify_streams': 'Spotify Streams'},
    title='Spotify Playlist Reach vs. Spotify Streams',
    template='plotly_dark',
    hover_name='track',
    hover_data={'artist': True, 'track_score': True},
)
scat1.update_traces(marker=dict(size=12, opacity=0.8))
st.plotly_chart(scat1)

# Create streamlit checkboxes for removing outlier x-variables
filter_tiktok_posts = st.checkbox('Show only songs with TikTok Posts < 15000000', value=False)

# Create filter conditions for scat2
filtered_scat2 = spotify_data.copy()
if filter_tiktok_posts:
    filtered_scat2 = filtered_scat2[filtered_scat2['tiktok_posts'] < 15000000]

# Create scatter plot 2
scat2 = px.scatter(
    filtered_scat2,
    x='tiktok_posts',
    y='spotify_streams',
    labels={'tiktok_posts': 'TikTok Posts', 'spotify_streams': 'Spotify Streams'},
    title='TikTok Posts vs. Streams',
    template='plotly_dark',
    hover_name='track',
    hover_data={'artist': True, 'track_score': True},
)
scat2.update_traces(marker=dict(size=12, opacity=0.8))
st.plotly_chart(scat2)
