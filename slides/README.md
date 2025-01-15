# PowerPoint to Quarto Converter

A Python script that converts PowerPoint presentations (.pptx) to Quarto RevealJS format (.qmd).

## Features

- Converts PowerPoint slides to Quarto RevealJS presentation format
- Preserves speaker notes and formats them according to Quarto's documentation
- Automatically extracts and saves images from slides
- Creates two-column layout for slides containing images (65% text, 35% images)
- Uses level 2 headers (##) for slide titles
- Maintains PowerPoint bullet points and text formatting
- Saves output files with the same name as input files (e.g., `lecture.pptx` → `lecture.qmd`)

## Requirements

- Python 3.x
- python-pptx
- python-slugify

## Setup Instructions

1. Create a virtual environment (only needed once):
```bash
cd slides  # Navigate to the slides directory
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install required packages (only needed once):
```bash
pip install python-pptx python-slugify
```

## Usage

1. Make sure your virtual environment is activated (see step 2 above)

2. Run the converter:
```bash
# If using the virtual environment's Python:
./venv/bin/python pptx_converter.py path/to/your/presentation.pptx

# Or if your virtual environment is activated:
python pptx_converter.py path/to/your/presentation.pptx
```

The script will:
1. Create an `images` subdirectory in the chapter folder (e.g., `ch01/images/`)
2. Extract all images from the PowerPoint and save them in the `images` directory
3. Generate a `.qmd` file with the same name as your PPTX file
4. Preserve any speaker notes from the PowerPoint in Quarto's `::: {.notes}` format

## Output Structure

For a PowerPoint file named `479-ch01-1_8.pptx`, the converter will:
1. Extract the chapter number (01) from the filename
2. Create directory structure if it doesn't exist:
   ```
   slides/
   ├── ch01/
   │   ├── source-files/      # Contains source presentation files
   │   │   ├── 479-ch01-1_8.pptx
   │   │   ├── 479-ch01-1_8.qmd
   │   │   └── main-source-ch1-1_8.md
   │   ├── notes/            # Contains generated note files
   │   │   └── (markdown notes)
   │   ├── audio/           # Contains generated audio files
   │   │   └── (mp3 files)
   │   └── images/          # Contains extracted images
   │       └── (presentation images)
   └── common/
       └── styles.css
   ```

## Adding Audio to Slides

After generating your audio files, follow these steps to add them to your Quarto slides:

1. File Structure:
   ```
   slides/
   ├── ch01/
   │   ├── source-files/
   │   │   ├── js/
   │   │   │   ├── audio-player.js
   │   │   ├── 479-ch01-1_8.qmd
   │   ├── audio/
   │   │   ├── 479-ch01-1_8_primary_focus.mp3
   │   │   ├── 479-ch01-1_8_engineering_contributions.mp3
   ```

2. Create the audio-player.js file in your chapter's js directory:
   ```javascript
   // Audio player functionality for Reveal.js slides
   document.addEventListener('DOMContentLoaded', function() {
       // Function to handle slide transitions
       function handleSlideTransition() {
           const currentSlide = Reveal.getCurrentSlide();
           const audio = currentSlide.querySelector('audio');
           
           if (audio) {
               // If slide has audio, play it and wait for completion
               audio.play().catch(e => console.log('Audio playback failed:', e));
               audio.addEventListener('ended', () => {
                   setTimeout(() => Reveal.next(), 1000); // Wait 1s after audio ends
               });
           } else {
               // If no audio, wait 5 seconds then advance
               setTimeout(() => Reveal.next(), 5000);
           }
       }

       // Configure Reveal.js
       Reveal.configure({
           autoSlide: 0, // Disable default auto-sliding
           loop: false,
           autoPlayMedia: false // We'll handle media playback
       });

       // Start presentation and handle first slide
       document.querySelector('#start-presentation').addEventListener('click', () => {
           document.querySelector('#start-overlay').style.display = 'none';
           handleSlideTransition();
       });

       // Listen for slide changes
       Reveal.on('slidechanged', handleSlideTransition);
   });
   ```

3. Update your QMD file's YAML header:
   ```yaml
   format: 
     revealjs:
       # Other settings...
       include-in-header:
         - text: |
             <script src="js/audio-player.js"></script>
             <div id="start-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center;">
                 <button id="start-presentation" style="padding: 20px 40px; font-size: 24px; cursor: pointer; background: #4CAF50; color: white; border: none; border-radius: 5px;">Start Presentation</button>
             </div>
   ```

4. Add audio to individual slides:
   ```markdown
   ## Your Slide Title

   - Your slide content here
   - More content

   <div class="audio-source" style="display: none;" data-slide="slide01">
   <audio preload="none">
     <source src="../audio/your-audio-file.mp3" type="audio/mpeg">
   </audio>
   </div>
   ```

5. Audio Behavior:
   - When you open the presentation, you'll see a "Start Presentation" button
   - Click the button to begin the presentation with audio
   - Audio plays automatically when each slide is shown
   - Slides advance automatically after:
     - Audio finishes playing (plus 1 second delay)
     - 5 seconds if there's no audio
   - You can still use arrow keys or space to manually control slides

6. File Paths:
   - Audio files: Use relative paths from your QMD file (e.g., `../audio/filename.mp3`)
   - JavaScript: Place in `js` directory next to your QMD file
   - Reference paths relative to the QMD file's location

This setup creates a professional presentation experience with automatic audio playback and slide transitions.

## Notes and Audio Generation

After converting the PowerPoint to Quarto format, you can generate comprehensive notes and audio files:

1. Create notes for each section:
   - Notes should be created in the `notes` directory within the chapter folder
   - Each note file should follow the naming convention: `chapterfile_section_notes.md`
   - Example: `479-ch01-1_8_primary_focus_notes.md`

2. Generate audio files from notes:
   - Use the audio generation script to convert notes to speech
   - Audio files will be created in the `audio` directory
   - Each audio file corresponds to its note file
   - Example: `479-ch01-1_8_primary_focus.mp3`

3. File Organization:
   - Source files (`.pptx`, `.qmd`, source `.md`) go in the `source-files` directory
   - Note files (`.md`) go in the `notes` directory
   - Audio files (`.mp3`) go in the `audio` directory
   - Images go in the `images` directory

This structure keeps the chapter folder organized and makes it easy to locate specific content types.

## Audio Generation Details

The audio files are generated using the ElevenLabs API. To use the audio generation script:

1. Set up ElevenLabs:
   - Create an account at [ElevenLabs](https://elevenlabs.io)
   - Get your API key from your account settings
   - Update the `API_KEY` in `generate_audio.py`

2. Configure Voice Settings:
   - Default voice ID: `WFP1Wqyc9POBM5u5N5gr`
   - Model: `eleven_multilingual_v2`
   - Settings:
     ```python
     "voice_settings": {
         "stability": 0.5,
         "similarity_boost": 0.75
     }
     ```
   - You can adjust these settings or choose a different voice in the script

3. Running the Script:
   ```bash
   # Make sure you're in the virtual environment
   source venv/bin/activate
   
   # Run the script
   python generate_audio.py
   ```

4. The script will:
   - Read all note files from your chapter directory
   - Generate an audio file for each note
   - Save the audio files in the chapter's `audio` directory
   - Use the same base filename as the note file

Remember to keep your API key secure and never commit it to version control.

## Troubleshooting

If you see "command not found: python" or similar errors:
1. Make sure you're using the Python from the virtual environment:
   ```bash
   ./venv/bin/python pptx_converter.py your_file.pptx
   ```
2. Or activate the virtual environment first:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   python pptx_converter.py your_file.pptx
   ```

## License

[Your chosen license]
