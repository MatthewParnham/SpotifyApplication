import sys
import spotipy
import spotipy.util as util
import os

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


if __name__ == '__main__':
    username = input("Enter your username: ")
    try:
        os.remove(".cache-"+username)
    except:
        pass
    token = util.prompt_for_user_token(username,
    scope='playlist-modify-private,user-top-read',
    client_id='d1eebb993a9849288e221d27b95158f5',
    client_secret='0115f96419b848c0a5e2e28d1257618e',
    redirect_uri='http://www.google.com')

    if token:
        sp = spotipy.Spotify(auth=token)
        playlist = sp.user_playlist_create(username, "mUSic Shared Playlist", public=False)
        tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')
        trackIDs = []
        for track in tracks['items']:
            trackIDs.append(track['uri'])
        sp.user_playlist_add_tracks(username, playlist_id=playlist['uri'], tracks=trackIDs)
    else:
        print("Can't get token for", username)
