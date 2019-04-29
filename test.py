# THIS PROGRAM DOES NOT RUN, FOR RESEARCH ONLY

import sys
import spotipy
import spotipy.util as util

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

#create playlist
#get id of playlist
#add ids of songs, for all the playlists
#compare the two lists of songs between the accounts
#add the ids of songs that are in both accounts to the playlist
#display the songs for the new playlsit

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists.py [username]")
        username = input("Spotify Username: 1247972725 ")

    token = util.prompt_for_user_token(username, client_id='d1eebb993a9849288e221d27b95158f5',
                                       client_secret='0115f96419b848c0a5e2e28d1257618e',
                                       redirect_uri='http://www.google.com')
    if token:
        sp = spotipy.Spotify(auth=token)
        id = "44eUqnNz6Jg96JP4ang0HJ"
        track = "0UyljEbX9dqI1K0sqdv6B6"
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    else:
        print("Can't get token for", username)
