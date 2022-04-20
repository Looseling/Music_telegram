from pytube import YouTube
import os

yt = YouTube('/watch?v=H0IKOM5973E')
mp3_file = yt.streams.filter(only_audio=True).first()
filename = mp3_file.default_filename
out_file = mp3_file.download('./singles')
new_file = os.getcwd() + './singles/' + filename[0:len(filename)-4] + '.mp3'

os.rename(out_file, new_file )