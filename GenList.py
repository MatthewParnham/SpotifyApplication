import sys
import spotipy
import spotipy.util as util

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


if __name__ == '__main__':
    username = input("Enter your username: ")

    token = util.prompt_for_user_token(username,
    scope='playlist-modify-private',
    client_id='d1eebb993a9849288e221d27b95158f5',
    client_secret='0115f96419b848c0a5e2e28d1257618e',
    redirect_uri='http://www.google.com')

    if token:
        sp = spotipy.Spotify(auth=token)
        playlist = sp.user_playlist_create(username, "mUSic Shared Playlist", public=False)
        trackIDs = ["1pAyyxlkPuGnENdj4g7Y4f", "7D2xaUXQ4DGY5JJAdM5mGP"]
        sp.user_playlist_add_tracks(username, playlist_id=playlist['uri'], tracks=trackIDs)
    else:
        print("Can't get token for", username)
