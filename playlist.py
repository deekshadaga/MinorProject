from pytube import YouTube,Playlist

def playlistdownload(url):
    p = Playlist(url)
    for video in p.videos:
        vid = video.streams.filter(progressive = True, file_extension = "mp4").first()
        vid.download('/home/new/Downloads')
    return "p success"