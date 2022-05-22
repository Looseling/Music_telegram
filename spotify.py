from __future__ import unicode_literals
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
from pytube import YouTube
import os
from config import *

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=Spotify_client_id,
                                                        client_secret=Spotify_client_secret))

class Song:
    def __init__(self, link):
        self.link = link
        self.song = spotify.track(link)
        self.trackName = self.song['name']
        self.artist = self.song['artists'][0]['name']
        self.artists = self.song['artists']
        self.trackNumber = self.song['track_number']
        self.album = self.song['album']['name']
        self.releaseDate = int(self.song['album']['release_date'][:4])
        self.duration = int(self.song['duration_ms'])

    def Features(self):
        if len(self.artists) > 1:
            features = "(Ft."
            for artistPlace in range(0, len(self.artists)):
                try:
                    if artistPlace < len(self.artists) - 2:
                        artistft = self.artists[artistPlace + 1]['name'] + ", "
                    else:
                        artistft = self.artists[artistPlace + 1]['name'] + ")"
                    features += artistft
                except:
                    pass
        else:
            features = ""
        return features

    def ConvertTimeDuration(self):
        seconds = (self.duration / 1000) % 60
        minutes = (self.duration / (1000 * 60)) % 60
        seconds = int(seconds)
        minutes = int(minutes)

        if seconds >= 10:
            time_duration1 = "{0}:{1}".format(minutes, seconds)
            time_duration2 = "{0}:{1}".format(minutes, seconds + 1)
            time_duration3 = "{0}:{1}".format(minutes, seconds - 1)
            time_duration4 = "{0}:{1}".format(minutes, seconds + 2)

            if seconds == 10:
                time_duration3 = "{0}:0{1}".format(minutes, seconds - 1)
            elif seconds == 58 or seconds == 59:
                time_duration4 = "{0}:0{1}".format(minutes + 1, seconds - 58)
                if seconds == 59:
                    time_duration2 = "{0}:0{1}".format(minutes + 1, seconds - 59)

        else:
            time_duration1 = "{0}:0{1}".format(minutes, seconds)
            time_duration2 = "{0}:0{1}".format(minutes, seconds + 1)
            time_duration3 = "{0}:0{1}".format(minutes, seconds - 1)
            time_duration4 = "{0}:0{1}".format(minutes, seconds + 2)
            if seconds == 9 or seconds == 8:
                time_duration4 = "{0}:{1}".format(minutes, seconds + 2)
                if seconds == 9:
                    time_duration2 = "{0}:{1}".format(minutes, seconds + 1)

            elif seconds == 0:
                time_duration3 = "{0}:{1}".format(minutes - 1, seconds + 59)
        return time_duration1, time_duration2, time_duration3, time_duration4


    def YTLink(self):
        results = list(YoutubeSearch(str(self.trackName + " " + self.artist)).to_dict())
        time_duration1, time_duration2, time_duration3, time_duration4 = self.ConvertTimeDuration()
        YTSlug = ''
        for URLSSS in results:
            timeyt = URLSSS["duration"]
            if timeyt == time_duration1 or timeyt == time_duration2 or timeyt == time_duration3 or timeyt == time_duration4:
                YTSlug = URLSSS['url_suffix']
                break

        YTLink = str("https://www.youtube.com/" + YTSlug)
        return YTLink




    def YTDownload(self, type):
        yt = YouTube(self.YTLink())

        mp3_file = yt.streams.filter(only_audio=True).first()
        if type == 'AL':
            out_file = mp3_file.download('./album')
            destination = './album/'
        elif type == 'S':
            out_file = mp3_file.download('./singles')
            destination = './singles/'

        try:
            new_file = os.getcwd() + destination + self.trackName + '.mp3'
            os.rename(out_file, new_file)
        except:
            self.trackName = mp3_file.default_filename[0:len(mp3_file.default_filename)-4]
            new_file = os.getcwd() + destination + self.trackName + '.mp3'
            os.rename(out_file, new_file)



def album(link):
    results = spotify.album_tracks(link)
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    return albums


def searchalbum(album_name):
    results = spotify.search(album_name)
    return results['tracks']['items'][0]['album']['external_urls']['spotify']


def searchsingle(track):
    results = spotify.search(track)
    return results['tracks']['items'][0]['external_urls']['spotify']

