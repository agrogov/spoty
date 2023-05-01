# spoty
Python script to synchronize two Spotify accounts

## objects to be synced
- user's saved tracks
- user's saved artists
- user's saved albums
- user's playlists

## requirements
- on each account create new app to be able to use Spotify API
  - open https://developer.spotify.com/dashboard and click on "Create app" button
  <img width="1460" alt="image" src="https://user-images.githubusercontent.com/5955205/235381934-5a7ee71b-bf80-409d-a983-4a78ea8bcefb.png">
  - click on "Settings" button
  <img width="1438" alt="image" src="https://user-images.githubusercontent.com/5955205/235382096-9c9abcc3-a875-46fe-b738-cb2ed73d755c.png">
  - copy "Client ID" and "Client secret" values
  <img width="1422" alt="image" src="https://user-images.githubusercontent.com/5955205/235382124-e22164c7-44d0-48cb-9f12-d97e19cf88a7.png">

- install spotipy lib
```bash
pip install spotipy
```

## usage
- change variables with your Spotify accounts emails and values from the previous step
```python
old_username = "your_old_account_email@outlook.com"
old_client_id = "OLD_CLIENT_ID"
old_client_secret = "OLD_CLIENT_SECRET"

new_username = "your_new_account_email@gmail.com"
new_client_id = "NEW_CLIENT_ID"
new_client_secret = "NEW_CLIENT_SECRET"
```
- run script, sequentially, pages for authorization will open in the browser, first in the old account, then in the new one. After authorization, you need to allow the application access to your account
```bash
python spoty.py
```
