import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy.util as util
import os
from random import randint

# Get the username from input
username = input("Enter your friend's Username: ")
friend_name = username

client_credentials_manager = SpotifyClientCredentials(client_id='d1eebb993a9849288e221d27b95158f5', client_secret='0115f96419b848c0a5e2e28d1257618e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists(username)
trackIDs1 = []
while playlists:
    for i, playlist in enumerate(playlists['items']):
        #print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
        tracks = results['tracks']

        for track in tracks['items']:
            trackIDs1.append(track['track']['uri'])
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None



sp = None



def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

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
        playlist = sp.user_playlist_create(username, "mUSic Playlist with " + friend_name, public=False)
        tracks = sp.current_user_top_tracks(limit=100, offset=0, time_range='medium_term')
        trackIDs2 = []
        for track in tracks['items']:
            trackIDs2.append(track['uri'])


        # Create new list!
        newList = intersection(trackIDs1,trackIDs2)

        while(len(newList) < 30):
            switch = True

            if(switch):
                randIdx = randint(0,len(trackIDs1)-1)
                if trackIDs1[randIdx] not in newList:
                    newList.append(trackIDs1[randIdx])
                    switch = False
            else:
                randIdx = randint(0,len(trackIDs2)-1)
                if trackIDs2[randIdx] not in newList:
                    newList.append(trackIDs2[randIdx])
                    switch = True

        sp.user_playlist_add_tracks(username, playlist_id=playlist['uri'], tracks=newList)
    else:
        print("Can't get token for", username)
