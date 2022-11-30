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

#we got access!

headers = {
    "Authorization": "Bearer " + token
}

artistId = "artistId"
list_of_artist = ["H.E.R.", "Summer Walker", "Jhené Aiko", "Ari Lennox", 
"Bryson Tiller", "Destinys Child", "Brent Faiyaz",
"Kehlani", "Drake", "Chris Brown", "Lucky Daye" ]
def get_artistID(list_of_artist):

    searchUrl = "https://api.spotify.com/v1/search"
    artistId_lst = []


    for artist in list_of_artist: 
        #print(artist)
        para = {
        "q" : artist,
        "type": "artist",
        "limit": "5"
        }
        r = requests.get(searchUrl, headers=headers, params = para)

        json_data = json.loads(r.text)
        if artist == json_data['artists']['items'][0]['name']:
            tup = (json_data['artists']['items'][0]['name'], json_data['artists']['items'][0]['id'])
            artistId_lst.append(tup)
            #internal_artistId = {json_data['artists']['items'][0]['name']:json_data['artists']['items'][0]['id']}
            #artistId_dic.update(internal_artistId)
            #json_data['artists']['items'][0]['id'] gives us artist id

        
    return artistId_lst


def get_topTracks(artistId_lst):

    para = {
    "market": 'US',
    "limit": "10"
    }
    toptracks_lst = []


    for id in artistId_lst:
        toptracksUrl = f"https://api.spotify.com/v1/artists/{id[1]}/top-tracks"
        #print(id[1])
        r = requests.get(toptracksUrl, headers=headers, params = para)
        json_data = json.loads(r.text)
        for i in range(0,10):
            tup = (id[1], id[0], json_data['tracks'][i]['name'],json_data['tracks'][i]['popularity'] )
            toptracks_lst.append(tup)
    return(toptracks_lst)

def get_table(data, filename):
    
    with open(filename, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Artist ID', 'Artist Name', 'Song Title', 'Song Popularity'])
        for row in data:
            csv_out.writerow(row)

def get_avg_popularity(data):
    popularity_tot_dic = {}
    for i in data: 
        if i[1] in popularity_tot_dic:
            popularity_tot_dic[i[1]] += int(i[3])
        else:
            popularity_tot_dic[i[1]] = int(i[3])

    avg_popularity = [] 
    for i in popularity_tot_dic.items():
        avg = int(i[1])/10
        artist = i[0]
        tup = (artist, avg)
        avg_popularity.append(tup)
    
    return avg_popularity

def get_table2(filename, data2):
    with open(filename, 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Artist Name', 'Average Song Popularity'])
        for row in data2:
            csv_out.writerow(row)

artistIdtup = get_artistID(list_of_artist)
data = get_topTracks(artistIdtup)
get_table(data, "topTracks.csv")
data2 = get_avg_popularity(data)
get_table2(data2, "AvgTopTracksPOPperArtist")

