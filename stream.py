import re
from pytube import YouTube, Search

# Define function to stream audio from youtube
def stream(search: str):
    if re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", search):
        yt = YouTube(search)
        audio = yt.streams.filter(only_audio=True).first()
        
        
        return audio.download(filename='sandro.mp3'), audio.title
    else:
        sc = Search(search)
        yt = sc.results[1]
        audio = yt.streams.filter(only_audio=True).first()
        
        return audio.download(filename='sandro.mp3'), audio.title
