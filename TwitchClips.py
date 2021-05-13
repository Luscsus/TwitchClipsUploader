from __future__ import unicode_literals
import requests
from datetime import datetime, timedelta
import youtube_dl
from googleapiclient.discovery import build
import google.auth
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

ClientID = "hvbypaumhng8r11j0l20qooi8b2mmy"
NumberOfClips = 6
urls = []
titles = []
channelUrls = []
FinalUrls = []

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

def UploadVideo():   
    # loggin into the channel
    channel = Channel()
    channel.login("client_secret.json", "credentials.storage")
    for x in range(NumberOfClips):
        # setting up the video that is going to be uploaded
        video = LocalVideo(file_path=FinalUrls[x])

        # setting snippet
        video.set_title(titles[x])
        video.set_description("This is a description")
        video.set_tags(["Twitch", "Clip"])
        video.set_category("gaming")
        video.set_default_language("en-US")

        # setting status
        video.set_embeddable(True)
        video.set_license("creativeCommon")
        video.set_privacy_status("private")
        video.set_public_stats_viewable(True)

        # uploading video and printing the results
        #video = channel.upload_video(video)
        print(video.id)
        print(video)

GetClip()
ConvertVideoToMp4()
UploadVideo()
