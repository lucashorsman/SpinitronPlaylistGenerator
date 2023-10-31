from bs4 import BeautifulSoup
import requests
import spotipy as sp
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


def parse_url():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.find_all(class_="spin-item")
    songs = []
    for element in elements:
        print(element.find(class_="artist").get_text())
        print(element.find(class_="song").get_text())
        songs.append(
            element.find(class_="artist").get_text()
            + " "
            + element.find(class_="song").get_text()
        )

    return songs


# main
# general setup
client_id = "14f23c99c6174bc7843cd7864abc22cc"
client_secret = "b2d3a6bbebe24e69a78b98a446471072"
scope = "playlist-modify-public"
token = util.prompt_for_user_token(
    None, scope, client_id, client_secret, redirect_uri="https://localhost:8080"
)
spotify = sp.Spotify(auth=token)
user = spotify.me()["id"]

# user input
url = input("Enter the Spinitron URL: ")
playlistName = input("Enter the name of the playlist: ")
description = input("Enter the description of the playlist(hit enter if you dont want to add a description): ")
# create a playlist
playlist = spotify.user_playlist_create(
    user, playlistName, public=True, collaborative=False, description=description
)

songByArtistinSpotify = []
songs = parse_url()
for song in songs:
    result = spotify.search(q=song, type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songByArtistinSpotify.append(uri)
    except IndexError:
        print(f"No results found for {song}")

spotify.playlist_add_items(
    playlist_id=playlist["id"], items=songByArtistinSpotify, position=None
)
