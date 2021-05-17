# TwitchClipsUploader
The goal of the project is to find the most popular daily clips on Twitch and upload them on youtube. 
# About the project:
At first I wanted to upload 10 clips from the 10 top categories of the previous day, but i found out that youtube api quota lets you use a maximum 10 000 units of api calls per day. And uploading a video consumes 1600 units, so you can only upload 6 videos per day. So now it only uploads the top 6 clips of the previous day every 4 hours over the course of a day.
# How it works:
The script first uses the twitch api to find the 6 most popular clips of the previous day. Takes the clips url, title and the channels url. Then it uses https://github.com/ytdl-org/youtube-dl to convert the clips url to an mp4 url and sets the videos description, title, tags and so on. After that we can upload it to youtube with https://github.com/jonnekaunisto/simple-youtube-api.
