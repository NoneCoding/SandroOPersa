from pytube import YouTube, Search

# Define function to stream audio from youtube
def stream(search: str):
    yt = YouTube(search)
    audio = yt.streams.filter(only_audio=True).first()
    
    return audio.download(filename='sandro.mp3')
