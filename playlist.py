#!/usr/bin/python3

import urllib.request
import urllib.error
import re
import sys
import time
import os
import cgi
import cgitb
import subprocess
#sys.path.insert(0,'/home/new/.local/bin/pytube')
from pytube import YouTube
#to show common error in browser
#cgitb.enable()


def getPageHtml(url):
    try:
        yTUBE = urllib.request.urlopen(url).read()
        return str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(1)

def getPlaylistUrlID(url):
    if 'list=' in url:
        eq_idx = url.index('list=') + 5
        pl_id = url[eq_idx:]
        if '&' in pl_id:
            amp = pl_id.index('&')
            pl_id = pl_id[:amp]
        return pl_id   
    else:
	#print("<div class='alert'>")
	#print("<span class='closebtn'>&times;</span>") 
	#print("<strong>Oops!</strong> ",url," is not a youtube playlist.")
	#print("</div>")
        print(url, "is not a youtube playlist.")
        exit(1)

def getFinalVideoUrl(vid_urls):
    final_urls = []
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_urls.append('https://www.youtube.com/' + vid_url[:url_amp])
    return final_urls

def getPlaylistVideoUrls(page_content, url):
    playlist_id = getPlaylistUrlID(url)

    vid_url_pat = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    vid_url_matches = list(set(re.findall(vid_url_pat, page_content)))

    if vid_url_matches:
        final_vid_urls = getFinalVideoUrl(vid_url_matches)
        print("Found",len(final_vid_urls),"videos in playlist.")
        printUrls(final_vid_urls)
        return final_vid_urls
    else:
        print('No videos found.')
        exit(1)

#function added to get audio files along with the video files from the playlist
def download_Video_Audio(path, vid_url, file_no):
    try:
        yt = YouTube(vid_url)
    except Exception as e:
        print("Error:", str(e), "- Skipping Video with url '"+vid_url+"'.")
        return
    try:
	# Tries to find the video in 720p
        #video = yt.get('mp4', '720p')
        video = yt.streams.filter(progressive = True, file_extension = "mp4").first()
    except Exception:  
        print("below 720p")
	# Sorts videos by resolution and picks the highest quality video if a 720p video doesn't exist
        video = sorted(yt.filter("mp4"), key=lambda video: int(video.resolution[:-1]), reverse=True)[0]

        print("downloading", yt.title+" Video and Audio...")
    try:
        #bar = progressBar()
        video.download(path)
        print("successfully downloaded", yt.title, "!")
    except OSError:
        print(yt.title, "already exists in this directory! Skipping video...")

def printUrls(vid_urls):
    for url in vid_urls:
        print(url)
        time.sleep(0.04)
        
if __name__ == '__main__':
	print("Content-type:text/html\r\n\r\n")
	print("<html>")
	print("<head><title> YouTube Extractor </title></head>")
	print("<link rel = 'stylesheet' type = 'text/css' href = 'stylesheet.css'>")
	print("<body>")
	print("<div class='bg'>")
	print("<br><br>")
	print("<div class='box' align='center'>")
	print("<h1 align='center'>Welcome to YouTube Extractor!</h1>")
	print("<hr>")
	print("<form method='post' action='playlist.py'>")
	print("<h3 align='center'>Please enter the link of youtube playlist that you want to download --></h3>")
	print("<input type='text' name='link' size=75><br>")
	print("<h3 align='center'>Please enter the location where you want to save it --></h3>")
	print("<input type='text' name='loc' size=75><br><br>")
	print("<input class='btn' type='submit' value='Download'/> ")
	print("</form>")
	print("</div>")
	form = cgi.FieldStorage()
	if form.getvalue("link"):
		url=form.getvalue("link")
		print("<div class='alert'>")
		print("<span class='closebtn'>&times;</span>") 
		print("<strong>yay!</strong>" +url+"<br>")
		print("<strong>yay!</strong>" +url+"<br>")
		print("<strong>yay!</strong>" +url+"<br>")
		print("<strong>yay!</strong>" +url)
		print("</div>")
	if form.getvalue("loc"):
		directory=form.getvalue("loc")
	else:
		directory=os.getcwd()

        # make directory if dir specified doesn't exist
	os.chdir('/home/new')
	try:
        	os.makedirs(directory, exist_ok=True)
	except OSError as e:
		print("<div class='alert'>")
		print("<span class='closebtn'>&times;</span>") 
		print("<strong>Oops!</strong>",e.reason)
		print("</div>")		
		#print(e.reason)
		exit(1)
	if not url.startswith("http"):
		url = 'https://' + url

	playlist_page_content = getPageHtml(url)
	vid_urls_in_playlist = getPlaylistVideoUrls(playlist_page_content, url)

        # downloads videos and audios
	for i,vid_url in enumerate(vid_urls_in_playlist):
		download_Video_Audio(directory, vid_url, i)
		time.sleep(1)
	print("</body></html>")

