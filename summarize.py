# summarize.py

import os

def summarize_transcript(transcript_text, client, model="gpt-4-turbo"):

    messages = [
        {"role": "system", 
         "content": "You are a helpful assistant that summarizes transcripts."},
        {"role": "user", 
         "content": f"Please summarize this transcript into a 800-1000 word summary. Feel free to use bullet points when appropriate.\n\n{transcript_text}"}
    ]

    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0.7)

    # Extract summary from the response
    return response.choices[0].message.content.strip()
