from __future__ import unicode_literals
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER

import glob

import numpy as np

import spotify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
import requests
import youtube_dl
from youtube_search import YoutubeSearch
import eyed3.id3
import eyed3

# mp3 = eyed3.load(f"./Tom Odell - Another Love (Official Video).mp4")
# # mp3 = YouTube(self.YTLink()).metadata
# # mp3.tag.artist = self.artist
# pprint(mp3.tag)


# extract the file names (with file paths)
filez = glob.glob("./Believer.mp3")
# loop through the mp3 files, extracting the track number,
# then setting the album, albumartist and track number
# to the appropriate values

print(filez)