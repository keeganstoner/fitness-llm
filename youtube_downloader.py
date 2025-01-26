# youtube_downloader.py

import os
import json
from googleapiclient.discovery import build
import yt_dlp

DOWNLOADED_VIDEOS_FILE = "downloaded_videos.json"
AUDIO_FOLDER = "audio"
COOKIES_FILE = "cookies.txt"

def load_downloaded_videos():
    if os.path.exists(DOWNLOADED_VIDEOS_FILE):
        with open(DOWNLOADED_VIDEOS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_downloaded_videos(video_ids):
    with open(DOWNLOADED_VIDEOS_FILE, 'w') as f:
        json.dump(list(video_ids), f)

def get_channel_videos(channel_id, api_key):
    """Retrieve all video IDs from a YouTube channel."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        type="video"
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"]
            })
        request = youtube.search().list_next(request, response)
    return videos

def get_playlist_videos(playlist_id, api_key):
    """Retrieve all video IDs from a YouTube playlist."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append({
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"]["title"],
                "channel_title": item["snippet"]["channelTitle"]
            })
        request = youtube.playlistItems().list_next(request, response)
    return videos

def download_audio(video_id):
    """Download audio track (mp3) for a specific video."""
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    ydl_opts = {
        'format': 'ba',  # best audio
        'outtmpl': f'{AUDIO_FOLDER}/{video_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': False,
        'verbose': True,
        'cookiefile': 'cookies.txt',
        # 'extractor_args': {"no-video-proxy": True}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
