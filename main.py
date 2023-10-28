
from bs4 import BeautifulSoup
import requests
import spotipy as sp
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


scope = "playlist-modify-public"
token = util.prompt_for_user_token('9h6llq95nilh7ifckssmamzmm',scope,client_id='14f23c99c6174bc7843cd7864abc22cc',client_secret='b2d3a6bbebe24e69a78b98a446471072',redirect_uri='https://localhost:8080')
spotify = sp.Spotify(auth=token)
url ='https://spinitron.com/KTUH/pl/18030348/In-The-Garage'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

elements = soup.find_all(class_='spin-item')

#create a playlist
playlist = spotify.user_playlist_create('In The Garage-Generated2', public=True, collaborative=False, description='')

songByArtist = []
for element in elements:
    print(element.find(class_='artist').get_text())
    print(element.find(class_='song').get_text())
    songByArtist.append(element.find(class_='artist').get_text() + ' ' + element.find(class_='song').get_text())

    

songByArtistinSpotify = []


for song in songByArtist:
    result = spotify.search(q=song, type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        songByArtistinSpotify.append(uri)
    except IndexError:
        print(f"No results found for {song}")



spotify.playlist_add_items(playlist_id=playlist['id'], items=songByArtistinSpotify, position=None)
