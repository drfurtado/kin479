import requests
import json
import os
from pathlib import Path

def generate_audio(text, filename):
    # API Configuration
    API_KEY = "sk_fc2bb47c436a4379a953859cf54e1438c5f064c7c818da74"  # Replace with your ElevenLabs API key
    VOICE_ID = "WFP1Wqyc9POBM5u5N5gr"  # You can change this to your preferred voice
    XI_API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    # Headers for the API request
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }

    # Prepare the request body
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        # Make the API request
        response = requests.post(XI_API_URL, json=body, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Create audio directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save the audio file
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Audio file {filename} generated successfully!")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    notes_dir = script_dir.parent / "slides" / "ch01"
    audio_dir = script_dir / "audio"

    # Create directories if they don't exist
    os.makedirs(notes_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)

    # Process all markdown files in the notes directory
    for note_file in notes_dir.glob("*_notes.md"):
        # Read the note content
        with open(note_file, 'r') as f:
            content = f.read()

        # Generate audio filename
        base_name = note_file.stem.replace("_notes", "")
        audio_file = audio_dir / f"{base_name}.mp3"

        # Generate audio from the note content
        generate_audio(content, str(audio_file))

if __name__ == "__main__":
    main()
