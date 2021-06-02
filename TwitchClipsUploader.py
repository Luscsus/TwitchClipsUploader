from __future__ import unicode_literals
import requests
import youtube_dl
from googleapiclient.discovery import build
import google.auth
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
import urllib.request
import os
import time

ClientID = "" # Put your youtube API ClientID here.
NumberOfClips = 6 # change the number if you have more youtube api qouta. Leave 6 if normal qouta amount.
urls = []
titles = []
channelUrls = []
FinalUrls = []

CurrentVideo = 0

def GetClip():
    # Get the 6 most popular clips of the day:
    for x in range(NumberOfClips):
        url = "https://api.twitch.tv/kraken/clips/top"
        headers = {
            "Client-ID": ClientID,
            "Accept": "application/vnd.twitchtv.v5+json"
        }
        params = {
            "first": NumberOfClips,
            "period": "day"
        }
        req = requests.get(url = url, headers = headers, params = params)
        clipData = req.json()

        # Save clip info:
        ViewCount = clipData["clips"][x]["views"]
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

# Download and save the videos to your working directory:
def SaveVideo():
    for x in range(NumberOfClips):
        print("Downloading video number " + str(x))
        urllib.request.urlretrieve(FinalUrls[x], str(x) + ".mp4") 

# Remove the videos from your working directory:
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
    video.set_description("Original clip: " + urls[CurrentVideoNumber] + ", \nClip uploader: " + channelUrls[CurrentVideoNumber] + ", This channel brings you the most popular twitch clips every 4 hours. \nYou can read more about how this works here: https://github.com/Luscsus/TwitchClipsUploader")
    video.set_tags(["Twitch", "Clip", "Streamer"])
    video.set_category(24) # You can find what category numbers mean what here: https://techpostplus.com/youtube-video-categories-list-faqs-and-solutions/
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("youtube")
    video.set_privacy_status("public")
    video.set_public_stats_viewable(True)

    # uploading video and printing the results
    CurrentVideo += 1
    video = channel.upload_video(video)
    print(video.id)
    print(video)

# First get the clips and store them in a list
GetClip()

# Convert the videos to mp4
ConvertVideoToMp4()

# Download the videos to the working directory
SaveVideo()

# Upload video every 4 hours
for x in range(NumberOfClips):
    try:
        print(CurrentVideo)
        UploadVideo(CurrentVideo)
    except: 
        print("The youtube api qouta has been exceded")
    time.sleep((24 / NumberOfClips) * 60 * 60)

CurrentVideo = 0

# Delete the videos from your working directory
RemoveVideo()
