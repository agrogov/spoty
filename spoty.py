import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

old_username = "your_old_account_email@outlook.com"
old_client_id = "OLD_CLIENT_ID"
old_client_secret = "OLD_CLIENT_SECRET"

new_username = "your_new_account_email@gmail.com"
new_client_id = "NEW_CLIENT_ID"
new_client_secret = "NEW_CLIENT_SECRET"

redirect_uri = "http://localhost:8080"

old_scopes = [
    "user-library-read",
    "user-follow-read",
    "playlist-read-collaborative",
    "playlist-read-private",
]

new_scopes = [
    "user-library-modify",
    "user-follow-modify",
    "playlist-modify-public",
    "playlist-modify-private",
    "user-library-read",
    "user-follow-read",
    "playlist-read-collaborative",
    "playlist-read-private",
]


def session_cache_path(account):
    return f"./sp_{account}_cache"


# Authenticate and authorize both accounts
print(f"{datetime.datetime.now()} Authenticate to OLD account")
sp_old = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        cache_path=session_cache_path("old"),
        client_id=old_client_id,
        client_secret=old_client_secret,
        redirect_uri=redirect_uri,
        scope=old_scopes,
        show_dialog=True,
    )
)

print(f"{datetime.datetime.now()} Authenticate to NEW account")
sp_new = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        cache_path=session_cache_path("new"),
        client_id=new_client_id,
        client_secret=new_client_secret,
        redirect_uri=redirect_uri,
        scope=new_scopes,
        show_dialog=True,
    )
)

# Get authentication tokens for both accounts
print(f"{datetime.datetime.now()} Get authentication token for OLD account")
if not sp_old.auth_manager.get_cached_token():
    sp_old_token_info = spotipy.util.prompt_for_user_token(
        username=old_username,
        scope=old_scopes,
        client_id=old_client_id,
        client_secret=old_client_secret,
        redirect_uri=redirect_uri,
        cache_path=session_cache_path("old"),
        show_dialog=True,
    )

print(f"{datetime.datetime.now()} Get authentication token for NEW account")
if not sp_new.auth_manager.get_cached_token():
    sp_new_token_info = spotipy.util.prompt_for_user_token(
        username=new_username,
        scope=new_scopes,
        client_id=new_client_id,
        client_secret=new_client_secret,
        redirect_uri=redirect_uri,
        cache_path=session_cache_path("new"),
        show_dialog=True,
    )

# Get user's saved tracks from old account
print(f"{datetime.datetime.now()} Getting tracks list from OLD account")
results = sp_old.current_user_saved_tracks()
tracks = results["items"]
while results["next"]:
    results = sp_old.next(results)
    tracks.extend(results["items"])

# Save tracks to new account
print(f"{datetime.datetime.now()} Saving tracks to NEW account")
for track in tracks:
    track_id = track["track"]["id"]
    # Check if track already exists in new account
    if not sp_new.current_user_saved_tracks_contains([track_id])[0]:
        sp_new.current_user_saved_tracks_add([track_id])

# Get user's saved artists from old account
print(f"{datetime.datetime.now()} Getting artists list from OLD account")
results = sp_old.current_user_followed_artists()
artists = results["artists"]["items"]
while results["artists"]["next"]:
    results = sp_old.next(results["artists"])
    artists.extend(results["artists"]["items"])

# Save artists to new account
print(f"{datetime.datetime.now()} Saving artists to NEW account")
for artist in artists:
    artist_id = artist["id"]
    # Check if artist already exists in new account
    if not sp_new.current_user_following_artists([artist_id])[0]:
        sp_new.user_follow_artists([artist_id])

# Get user's saved albums from old account
print(f"{datetime.datetime.now()} Getting albums list from OLD account")
results = sp_old.current_user_saved_albums()
albums = results["items"]
while results["next"]:
    results = sp_old.next(results)
    albums.extend(results["items"])

# Save albums to new account
print(f"{datetime.datetime.now()} Saving albums to NEW account")
for album in albums:
    album_id = album["album"]["id"]
    # Check if album already exists in new account
    if not sp_new.current_user_saved_albums_contains([album_id])[0]:
        sp_new.current_user_saved_albums_add([album_id])

# Get user's playlists from old account
print(f"{datetime.datetime.now()} Getting playlists list from OLD account")
results = sp_old.current_user_playlists()
playlists = results["items"]
while results["next"]:
    results = sp_old.next(results)
    playlists.extend(results["items"])

# Create playlists in new account and add tracks
print(f"{datetime.datetime.now()} Saving playlists to NEW account")
for playlist in playlists:
    playlist_name = playlist["name"]
    # Check if playlist already exists in new account
    existing_playlists = sp_new.current_user_playlists()["items"]
    existing_playlist_names = [p["name"] for p in existing_playlists]
    if playlist_name in existing_playlist_names:
        # Get existing playlist ID
        new_playlist_id = [
            p["id"] for p in existing_playlists if p["name"] == playlist_name
        ][0]
    else:
        # Create new playlist in new account
        new_playlist = sp_new.user_playlist_create(
            user=sp_new.current_user()["id"],
            name=playlist_name,
            public=playlist["public"],
        )
        new_playlist_id = new_playlist["id"]
    # Get tracks from old playlist
    results = sp_old.playlist_items(playlist["id"])
    tracks = results["items"]
    while results["next"]:
        results = sp_old.next(results)
        tracks.extend(results["items"])
    # Add tracks to new playlist in chunks of 100
    track_ids = [track["track"]["id"] for track in tracks]
    for i in range(0, len(track_ids), 100):
        sp_new.playlist_add_items(
            playlist_id=new_playlist_id, items=track_ids[i: i + 100]
        )

print(f"{datetime.datetime.now()} We're done!")
