import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Get the username from input
username = input("Spotify Username: ")

client_credentials_manager = SpotifyClientCredentials(client_id='d1eebb993a9849288e221d27b95158f5', client_secret='0115f96419b848c0a5e2e28d1257618e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists(username)
trackIDs = []
while playlists:
    for i, playlist in enumerate(playlists['items']):
        #print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
        tracks = results['tracks']

        for track in tracks['items']:
            trackIDs.append(track['track']['uri'])
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
