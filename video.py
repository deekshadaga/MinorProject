from pytube import YouTube

def videodownload(url):
    yt = YouTube(url)
    vid = yt.streams.filter(progressive = True, file_extension = "mp4").first()
    vid.download('/home/new/Downloads')
    return "succss"

