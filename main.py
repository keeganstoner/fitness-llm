# main.py

import os
from tqdm import tqdm
from youtube_downloader import (
    load_downloaded_videos, 
    save_downloaded_videos,
    get_channel_videos, 
    get_playlist_videos,
    download_audio
)
from transcribe import transcribe_audio
from summarize import summarize_transcript

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')


from openai import OpenAI
client = OpenAI(api_key=OPENAI_KEY)

import warnings

# Suppress the specific warnings
warnings.filterwarnings("ignore", message=".*You are using torch.load with weights_only=False.*")
warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*")


def main():
    # summary_file = "summaries.txt"
    summaries_folder = "summaries"
    os.makedirs(summaries_folder, exist_ok=True)
    downloaded_set = load_downloaded_videos()
    
    # all_videos = get_channel_videos(CHANNEL_ID, YOUTUBE_API_KEY)
    all_videos = get_playlist_videos(PLAYLIST_ID, YOUTUBE_API_KEY)
    new_videos = [v for v in all_videos if v["video_id"] not in downloaded_set]
    
    for video in tqdm(new_videos, desc="Processing new videos"):
        video_id = video["video_id"]
        video_title = video["title"]
        channel_title = video["channel_title"]

        if video_id in downloaded_set:
            print(f"Skipping already processed video: {video_id}")
            continue
        
        print(f"Processing {video_id}...")
        try:
            # Download
            download_audio(video_id)
            
            # Transcribe
            transcript = transcribe_audio(video_id)
            
            # Summarize
            summary = summarize_transcript(transcript, client)
            
            # # Append summary to file
            # with open(summary_file, "a", encoding="utf-8") as f:
            #     f.write(f"VIDEO ID: {video_id}\n")
            #     f.write(f"TITLE: {video_title}\n")
            #     f.write(summary + "\n\n---\n\n")
            
            
            # Save summary to a new file
            summary_filename = f"{video_title}.txt"
            summary_filepath = os.path.join(summaries_folder, summary_filename)
            with open(summary_filepath, "w", encoding="utf-8") as f:
                f.write(f"VIDEO ID: {video_id}\n")
                f.write(f"TITLE: {video_title}\n")
                f.write(f"CHANNEL: {channel_title}\n")
                f.write(summary + "\n\n---\n\n")
            

            # Optional: keep or remove full transcript. 
            # For memory’s sake, we won't keep it. 
            # If you want to keep it, just write to a separate transcript file.
            
            # Remove audio file to save space
            audio_path = f"audio/{video_id}.mp3"
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            # Mark as done
            downloaded_set.add(video_id)
            save_downloaded_videos(downloaded_set)


        except Exception as e:
            print(f"Error processing {video_id}: {e}")

if __name__ == "__main__":
    main()
