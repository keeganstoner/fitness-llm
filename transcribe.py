# transcribe.py

import whisper
import os

def transcribe_audio(video_id, model_name="base", audio_folder="audio"):
    """Transcribe mp3 file using Whisper."""
    model = whisper.load_model(model_name)
    audio_file = os.path.join(audio_folder, f"{video_id}.mp3")
    result = model.transcribe(audio_file)
    return result["text"]
