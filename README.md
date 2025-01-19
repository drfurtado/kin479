# KIN 479: Motor Control

This repository contains course materials for KIN 479: Motor Control.

## Setup for Audio Generation

To generate audio files for the course materials, you'll need to:

1. Install required Python packages:
```bash
pip install python-dotenv requests
```

2. Create a `.env` file in the root directory with the following variables:
```
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_VOICE_ID=your_preferred_voice_id  # Optional, defaults to WFP1Wqyc9POBM5u5N5gr
```

3. Never commit your `.env` file to version control - it's already in .gitignore to prevent accidental commits.

## Course Structure

The course materials are organized as follows:
- `slides/`: Course presentation slides
- `scripts/`: Utility scripts for content generation
- `notes-audio-files/`: Audio generation scripts for course notes
