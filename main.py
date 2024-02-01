import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = """Enter your client id"""
CLIENT_SECRET = """Enter your client secret"""
REDIRECT_URL = "http//:example.com"

date = input("What year do you want to travel to? Format: YYYY-MM-DD ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
html = response.text

soup = BeautifulSoup(html,'html.parser')

songs_titles = [x.getText().strip() for x in soup.find_all("h3",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")]

# print(songs_titles)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True,
                                               ))

user_id = sp.current_user()['id']

year = date.split("-")[0]
song_uris = []
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id,name=f"{date}_Billboard_top_100",public=False)

sp.playlist_add_items(playlist_id=playlist['id'],items=song_uris)


