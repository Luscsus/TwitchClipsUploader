# TwitchClipsUploader
The goal of the project is to find the most popular daily clips on Twitch and upload them on youtube. Here is the link to the youtube channel: 
# About the project:
At first I wanted to upload 10 clips from the 10 top categories of the day, but i found out that youtube api quota lets you use a maximum 10 000 units of api calls per day. And uploading a video consumes 1600 units, so you can only upload 6 videos per day. So now it only uploads the top 6 clips of the day every 4 hours over the course of a day.
# How it works:
The script first uses the twitch api to find the 6 most popular clips of the previous day. Takes the clips url, title and the channels url. Then it uses https://github.com/ytdl-org/youtube-dl to convert the clips url to an mp4 url and sets the videos description, title, tags and so on. After that we can upload it to youtube with https://github.com/jonnekaunisto/simple-youtube-api. The script is hosted on https://www.heroku.com.
# Requirements:
- Python 3.9+
- youtube_dl (pip install youtube_dl)
- simple_youtube_api (pip install simple-youtube-api)
# How to use:
1. First fork this repository.
2. Follow the guide here: https://support.google.com/cloud/answer/6158849?hl=en#zippy=%2Cuser-consent%2Cpublic-and-internal-applications%2Cauthorized-domains. And download the client secret key to your forked repository.
3. Create a twitch aplication here: https://dev.twitch.tv/console/apps. Set the name, set the Oauth Redirect URL to https://localhost, set the category to Analytics tool.
4. Open the TwitchClipsUploader.py script and set the variable ClientID to your Twitch application client ID.
5. Complete the youtube audit form here: https://support.google.com/youtube/contact/yt_api_form?hl=en (If you don't do this your videos will be set to private)
6. Deploy to heroku:
<a href="https://heroku.com/deploy?template=https://github.com/Luscsus/TwitchClipsUploader">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>

WORK IN PROGRESS
