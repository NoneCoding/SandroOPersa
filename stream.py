import youtube_dl


def stream(search):
    """
    Fetches necessary info to stream audio from youtube

    """
    options = {
        "prefer_ffmpeg": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "format": "best",
        "noplaylist": True,
        "default_search": "auto"
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        # Returns the url in the dict that extract_info got
        return ydl.extract_info(search, download=False)["entries"]
