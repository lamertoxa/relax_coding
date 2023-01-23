import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = ''' CLIENT ID '''
CLIENT_SECRET = ''' CLIENT SECRET CODE '''

scope_modify = "playlist-modify-public"
url = "https://www.billboard.com/charts/hot-100/"

sp_r = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    redirect_uri="http://example.com",
                    scope=scope_modify
                    ))

id_user = sp_r.current_user()["id"]

textInput = "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
birth = input(textInput)
birthYear = birth.split("-")[0]

response_bb = requests.get(url+birth)

soup = BeautifulSoup(response_bb.text, "html.parser")

song = soup.select("ul li h3.c-title")
author = soup.select("div ul li ul li span.u-max-width-330")
listSongs = []

for i in range (len(song)):
    listSongs.append(f"{song[i].getText().strip()} {author[i].getText().strip()}")

response_sp = sp_r.user_playlist_create(user=id_user,name=f"Hot-100 {birthYear} Year",public=True)

link_sp = response_sp["external_urls"]["spotify"]

playlist_id = response_sp["uri"]


for song in listSongs:
    current_track = sp_r.search(q=song,type="track",limit = 1)
    try:
        uri_track = [current_track["tracks"]["items"][-1]["uri"].replace("spotify:track:","")]
    except IndexError:
        continue
    response_track = sp_r.playlist_add_items(playlist_id=playlist_id,items=uri_track)

print (f"Copy this link and listen!\n{link_sp}")

