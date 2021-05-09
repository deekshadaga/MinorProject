from pytube import YouTube

def audiodownload(url):
    yt=YouTube(url)
    a=yt.streams.filter(only_audio=True).first()
    a.download('/home/new/Downloads')
    return "a success"

