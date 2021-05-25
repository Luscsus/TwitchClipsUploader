from __future__ import unicode_literals
import requests
from datetime import datetime, timedelta
import youtube_dl
from googleapiclient.discovery import build
import google.auth
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
import urllib.request
import os
import time

ClientID = ""
NumberOfClips = 6
urls = []
titles = []
channelUrls = []
FinalUrls = []

CurrentVideo = 0
now = datetime.now()
new_date = now - timedelta(days=1)
StartingTime = new_date.strftime("%Y-%m-%dT00:00:00Z")
EndingTime = now.strftime("%Y-%m-%dT00:00:00Z")

def GetClip():
    # Gets the most popular clips:
    for x in range(NumberOfClips):
        url = "https://api.twitch.tv/kraken/clips/top"
        headers = {
            "Client-ID": ClientID,
            "Accept": "application/vnd.twitchtv.v5+json"
        }
        params = {
            "first": NumberOfClips,
            "started_at": StartingTime,
            "ended_at": EndingTime
        }
        req = requests.get(url = url, headers = headers, params = params)
        clipData = req.json()
        ViewCount = clipData["clips"][x]["views"]
        if (ViewCount > 1000):
            urls.append(clipData["clips"][x]["url"])
            titles.append(clipData["clips"][x]["title"])
            channelUrls.append(clipData["clips"][x]["curator"]["channel_url"])
            
def ConvertVideoToMp4():
    for x in range(NumberOfClips):
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

        with ydl:
            result = ydl.extract_info(
                urls[x],
                download=False # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        FinalUrls.append(video["formats"][-1]["url"])

def SaveVideo():
    for x in range(NumberOfClips):
        print("Downloading video number " + str(x))
        urllib.request.urlretrieve(FinalUrls[x], str(x) + ".mp4") 

def RemoveVideo():
    for x in range(NumberOfClips):
        print("Deleting video number " + str(x))
        os.remove(str(x) + ".mp4")

def UploadVideo(CurrentVideoNumber): 
    # loggin into the channel
    channel = Channel()
    channel.login("client_secret.json", "credentials.storage")
    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path= str(CurrentVideo) + ".mp4")

    # setting snippet
    video.set_title(titles[CurrentVideoNumber])
    video.set_description("Original clip: " + urls[CurrentVideoNumber] + ", Original channel: " + channelUrls[CurrentVideoNumber] + ", This channel brings you the most popular twitch clips every 4 hours. You can read more about how this works here: https://github.com/Luscsus/TwitchClipsUploader")
    video.set_tags(["Twitch", "Clip", "Streamer"])
    video.set_category(24)
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("youtube")
    video.set_privacy_status("public")
    video.set_public_stats_viewable(True)

    # uploading video and printing the results
    video = channel.upload_video(video)
    #CurrentVideo += 1
    print(video.id)
    print(video)

while True:
    # First get the clips and store them in a list
    GetClip()
    # Convert the videos to mp4
    ConvertVideoToMp4()
    # Download the videos to the working directory
    SaveVideo()
    # Upload video every 4 hours
    for x in range(NumberOfClips):
        UploadVideo(CurrentVideo)
        time.sleep(864000)
    CurrentVideo = 0
    # Delete the videos from your working directory
    RemoveVideo()
