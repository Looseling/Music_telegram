from pytube import YouTube
import os

yt = YouTube('/watch?v=H0IKOM5973E')
mp3_file = yt.streams.filter(only_audio=True).first()
type = 'AL'
if type == 'AL':
    out_file = mp3_file.download('./album')
print(mp3_file)