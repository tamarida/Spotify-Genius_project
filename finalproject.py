import unittest
import requests
import base64
import json
import csv
import os

from secrets import *

# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

#Code above give us access to the Spotify API now we have to make requests!

headers = {
    "Authorization": "Bearer " + token
}

list_of_artist = ["H.E.R.", "Summer Walker", "Jhené Aiko", "Ari Lennox", 
"Bryson Tiller", "Destinys Child", "Brent Faiyaz",
"Kehlani", "Drake", "Chris Brown", "Lucky Daye" ]

def get_artistID(list_of_artist):
    """This function get_artistID takes in a list of artist names,
    searches the Spotify API for that artist, and
    returns a list if tuples of the (Artist Name, Artist ID)"""

    searchUrl = "https://api.spotify.com/v1/search"
    artistId_lst = []


    for artist in list_of_artist: 
        para = {
        "q" : artist,
        "type": "artist",
        "limit": "5"
        } #these are the parameters for searching in the Spotify API
        r = requests.get(searchUrl, headers=headers, params = para)
        json_data = json.loads(r.text) #takes results from request and turns it into a python dictionary object

        if artist == json_data['artists']['items'][0]['name']:
        # ^if the artists name is the same as the artist name in the results
            tup = (json_data['artists']['items'][0]['name'], json_data['artists']['items'][0]['id'])
            #^creat a tuple of the artist name and artist id
            artistId_lst.append(tup)
            #^add tuple to list

    return artistId_lst



def get_topTracks(artistId_lst):
    """The function get_topTracks takes in a list of tuples that contain (Artist Name, Artist ID),
    uses the top tracks Spotify API and the Artist ID 
    to return a list of tuples that have the artist name, artist ID, song title, song popularity
    with 10 songs (their top songs) per artist
    Ex. (Artist ID, Artist Name, Song Title (1), Song Popularity)
        (Artist ID, Artist Name, Song Title (2), Song Popularity) 
        etc... """

    para = {
    "market": 'US',
    "limit": "10"
    } #these are parameters for top tracks results in the Spotify API
    toptracks_lst = []


    for id in artistId_lst: #id is tuple of artist name(id[0]) and artist ID(id[1])
        toptracksUrl = f"https://api.spotify.com/v1/artists/{id[1]}/top-tracks"

        r = requests.get(toptracksUrl, headers=headers, params = para)
        json_data = json.loads(r.text)
        #^requests and load results into a python object

        for i in range(0,10): 
        #^give us the top ten tracks
            tup = (id[1], id[0], json_data['tracks'][i]['name'],json_data['tracks'][i]['popularity'] )
            #^create a tup and add (Artist ID, Artist Name, Song Title) 
            toptracks_lst.append(tup)
            #^add tuple to list

    return(toptracks_lst)



def get_table(data, filename):
    """This function get_table takes in a list of tuples and a filename 
    and creats a table 'topTracks.csv' """
    
    with open(filename, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Artist ID', 'Artist Name', 'Song Title', 'Song Popularity'])
        for row in data:
            csv_out.writerow(row)




def get_avg_popularity(data):
    """The function get_avg_popularity takes in a list of tuples(from get_topTracks) 
    and calculates the average song popularity using the Artist's top ten tracks, 
    then stores in a list of tuples avg_popularity with the Artist Name: Average Song Popularity in a key value pair"""
    popularity_tot_dic = {}
    for i in data: 
        if i[1] in popularity_tot_dic:
            popularity_tot_dic[i[1]] += int(i[3])
        else:
            popularity_tot_dic[i[1]] = int(i[3])
    #^creats a song popularity total dictionary per artist dictionary

    avg_popularity = [] 
    for i in popularity_tot_dic.items():
        avg = int(i[1])/10
        artist = i[0]
        tup = (artist, avg)
        avg_popularity.append(tup)
    #^uses the total popularity dictionary and calculates average per artist and add tuple into list
    
    return avg_popularity

def get_something(data):

    search_term = "Beyonce"
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

    r = requests.get(genius_search_url)
    json_data = json.loads(r.text)
    
    print(json_data['response']['hits'][1]['result']['api_path'])




artistIdtup = get_artistID(list_of_artist)
data = get_topTracks(artistIdtup)
get_table(data, "topTracks.csv")
avg_popularity = get_avg_popularity(data)
get_something(data)
