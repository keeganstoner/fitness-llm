# fitness-llm
Summarizes youtube videos.

Put info in `keys.py`:

```
YOUTUBE_API_KEY = <>
CHANNEL_ID = <>
OPENAI_KEY = <>
PLAYLIST_ID = <>
```

A few things you need:
- Openai API credits
- If any videos are age-restricted, you might need to download a `cookies.txt` file using a browser extension (search for this) and put it here

Given the `PLAYLIST_ID` (appears after `list=` in the playlist url), this will check for any new videos that have not yet been summarized and summarize them. 

Here's what it does:
1. Downloads the audio file using `yt_dlp`.
2. Transcribes the audio using openai Whisper (this is because the youtube autmatic transcripts are really bad)
3. Runs the full transcript through a prompted gpt-4-turbo instance to summarize it and place the summary in `summaries/`
4. Deletes all the old files to save space