
import os
import requests
import spotipy

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


# .env file se Spotify ki settings parhein
load_dotenv()

# User se chart ki date lein
date = input("Enter a date (YYYY-MM-DD): ")

# Billboard Hot 100 ka page
url = f"https://www.billboard.com/charts/hot-100/{date}/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=20
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Billboard se song titles hasil karein
song_elements = soup.select("li ul li h3")

song_names = []

for element in song_elements:
    song = element.get_text(strip=True)

    if song and song not in song_names:
        song_names.append(song)

if not song_names:
    print("No songs found. Billboard may have changed its page.")
    raise SystemExit

print(f"Songs found: {len(song_names)}")

# Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        cache_path=".spotify_cache"
    )
)

# Spotify par songs search karein
track_uris = []

for song in song_names:
    results = sp.search(
        q=f"track:{song}",
        type="track",
        limit=1
    )

    tracks = results["tracks"]["items"]

    if tracks:
        track_uris.append(tracks[0]["uri"])
        print("Found:", song)
    else:
        print("Not found:", song)

# Playlist banayein
if track_uris:
    user_id = sp.current_user()["id"]

    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"Billboard Hot 100 - {date}",
        public=False,
        description=f"Billboard chart songs for {date}"
    )

    # Tracks ko playlist mein add karein
    for start in range(0, len(track_uris), 100):
        batch = track_uris[start:start + 100]

        sp.playlist_add_items(
            playlist_id=playlist["id"],
            items=batch
        )

    print("\nPlaylist created successfully!")
    print(playlist["external_urls"]["spotify"])

else:
    print("No matching Spotify songs were found.")
