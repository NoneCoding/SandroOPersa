import youtube_dl


def stream(search):
    """
    Fetches necessary info to stream audio from youtube

    """
    options = {
        "prefer_ffmpeg": True,
        "format": "best",
        "noplaylist": True,
        "default_search": "auto",
        "age_limit": 20
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        # Returns the url in the dict that extract_info got
        return ydl.extract_info(search, download=False)["entries"]
