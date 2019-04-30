import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy.util as util
import os
from random import randint

# Get friend's username from input
username = input("Enter your friend's Username: ")
# Store as separate variable for later
friend_name = username

# Pass in Keys
client_credentials_manager = SpotifyClientCredentials(client_id='d1eebb993a9849288e221d27b95158f5', client_secret='0115f96419b848c0a5e2e28d1257618e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get Friend's public playlists
# This is a work around to authenticating both users.  A user's public playlist
#   is like to reflect listening habits as well as top tracks
# sp.user_playlists() sends an http GET request to spotify api and retrieves
#   the user's playlists in json format
playlists = sp.user_playlists(username)
trackIDs1 = []
# Cleaning up the data and adding every song's ID to the trackIDs1 list
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


# Resetting sp variable so it can be used again for the authenticated user
#   *Leaving this out can cause bugs*
sp = None


# Function: intersection - Takes 2 lists as parameters and returns a list containing
#   the intersection of the two
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


if __name__ == '__main__':
    # Main user enters spotify username
    username = input("Enter your username: ")
    # When creating a an authentication token, spotipy stores it for later use
    #   This causes the program to crash, so we delete it if it exists before
    #   Continuing
    try:
        os.remove(".cache-"+username)
    except:
        pass

    # Getting our token from Spotify api
    #   With permissions to modify the user's private playlists as well as access
    #   his/hers top tracks
    token = util.prompt_for_user_token(username,
    scope='playlist-modify-private,user-top-read',
    client_id='d1eebb993a9849288e221d27b95158f5',
    client_secret='0115f96419b848c0a5e2e28d1257618e',
    redirect_uri='http://www.google.com')

    if token:
        # Create a spotify object with the authenticated token
        sp = spotipy.Spotify(auth=token)
        # Create a new playlist for the authenticated user
        playlist = sp.user_playlist_create(username, "mUSic Playlist with " + friend_name, public=False)
        # http GET message to retrieve the user's top 100 tracks
        #       time_range can be changed to 'short_term', 'medium_term', or 'long_term'
        #       depending on prefernce
        tracks = sp.current_user_top_tracks(limit=100, offset=0, time_range='medium_term')
        trackIDs2 = []
        # Populate trackIDs2 with this user's top tracks
        for track in tracks['items']:
            trackIDs2.append(track['uri'])


        # Create new list containing only songs found in both user's listening habits
        newList = intersection(trackIDs1,trackIDs2)

        # If this list is not long enough, we can populate it with random songs
        #       alternating between both users until we hit the minimum threshold
        #       of 30 songs
        switch = True
        while(len(newList) < 30):

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

        # Adds the list of songs to the previously created playlist
        sp.user_playlist_add_tracks(username, playlist_id=playlist['uri'], tracks=newList)
        print()
        print("Playlist Created") # Notes completion of process in console
    else:
        print("Can't get token for", username)
