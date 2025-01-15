import requests
import json
import os
import time
from pathlib import Path

# Configuration
API_KEY = "sk_fc2bb47c436a4379a953859cf54e1438c5f064c7c818da74"  # Your ElevenLabs API key
VOICE_ID = "WFP1Wqyc9POBM5u5N5gr"  # You can change this to your preferred voice
XI_API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def generate_audio(text, output_path):
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
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save the audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Audio file {output_path} generated successfully!")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def read_note_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    # Setup paths
    base_dir = Path(__file__).parent.parent
    notes_dir = base_dir / "slides" / "ch01" / "notes"
    audio_dir = base_dir / "slides" / "ch01" / "audio"
    
    # Create audio directory if it doesn't exist
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Delete existing audio files
    for audio_file in audio_dir.glob("*.mp3"):
        print(f"Removing existing audio file: {audio_file}")
        audio_file.unlink()
    
    # Process each note file
    for note_file in notes_dir.glob("479-ch01-1_8_*_notes.md"):
        # Extract the identifier from the filename
        identifier = note_file.stem.replace('_notes', '')
        output_path = audio_dir / f"{identifier}.mp3"
        
        print(f"Processing {identifier}...")
        text = read_note_file(note_file)
        
        if generate_audio(text, str(output_path)):
            print(f"Successfully generated audio for {identifier}")
            # Sleep to avoid rate limiting
            time.sleep(3)
        else:
            print(f"Failed to generate audio for {identifier}")
            break

if __name__ == "__main__":
    main()
