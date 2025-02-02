# Slide Implementation Instructions

This document provides instructions for implementing Quarto presentations for the KIN479 course, based on successful implementations.

## Directory Structure

```
slides/
├── ch01/
│   ├── source-files/      # Contains Quarto files
│   │   ├── js/           # JavaScript files
│   │   │   └── audio-player.js
│   │   └── 479-ch01-1_8.qmd
│   └── audio/            # Contains audio files
│       └── 479-ch01-1_8_*.mp3
│   ├── flashcards/
│   │   ├── 479-ch01-1_8-1-flashcards.qmd  # Part 1 flashcards
│   │   ├── 479-ch01-1_8-2-flashcards.qmd  # Part 2 flashcards
│   │   └── ...
│   └── quizzes/
│       ├── 479-ch01-1_8-1-quiz.qmd  # Part 1 quiz
│       ├── 479-ch01-1_8-2-quiz.qmd  # Part 2 quiz
│       └── ...
```

## Quarto File Structure

### YAML Header
```yaml
---
title: "Chapter Title"
subtitle: "Subtitle"

author:
  - name: Author Name
    title: Title
    department: Department
    orcid: ORCID
    email: Email
    affiliations: Institution

# Document Settings
date: last-modified
logo: "images/logos/logo.png"

format: 
  revealjs:
    theme: default
    width: 1600
    height: 900
    margin: 0.1
    controls: true
    navigation-mode: linear
    menu: true
    menu-position: left
    slide-level: 2

include-in-header:
  - text: |
      <style>
      </style>
      <script>
      window.addEventListener('load', function() {
          Reveal.configure({ keyboard: false });
      });
      </script>
      <script src="js/audio-player.js"></script>
      <div id="start-overlay">...</div>
---
```

### Slide Structure
Each slide should follow this structure:
```markdown
## Slide Title

:::: {.columns}

::: {.column width="50%"}
- Bullet point 1
- Bullet point 2
- Bullet point 3
:::

::: {.column width="50%"}
:::
:::

::::

<div class="audio-source" style="display: none;">
<audio preload="none" controls>
<source src="../audio/479-ch01-1_8_slide_name.mp3" type="audio/mpeg">
Your browser does not support the audio element. </audio>
</div>

::: notes
Detailed speaker notes that match the audio content
:::
```

## Important Guidelines

1. **Audio Files**
   - Place in `audio` directory
   - Use naming convention: `479-ch01-1_8_slide_name.mp3`
   - Audio paths should be relative: `../audio/`

3. **Layout**
   - Use two-column layout with 50% width each
   - Left column for bullet points
   - Right column for content
   - Keep bullet points concise and clear

4. **Notes**
   - Include detailed speaker notes for each slide
   - Notes should match audio content
   - Use conversational, engaging tone

## Slide Design Guidelines

### Images and Icons

1. **Using Font Awesome Icons**
   - Include Font Awesome in your YAML header:
     ```yaml
     format:
       revealjs:
         include-in-header:
           - text: |
               <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
     ```
   - Use icons in your slides:
     ```markdown
     <i class="fas fa-brain fa-2x"></i>  <!-- Brain icon -->
     <i class="fas fa-running fa-2x"></i> <!-- Running person -->
     <i class="fas fa-dumbbell fa-2x"></i> <!-- Dumbbell -->
     ```
   - Size options: fa-xs, fa-sm, fa-lg, fa-2x through fa-10x
   - Browse icons at [Font Awesome](https://fontawesome.com/icons)

2. **Icon Styling**
   - Add color:
     ```markdown
     <i class="fas fa-brain fa-2x" style="color: #ff0000;"></i>
     ```
   - Center icons:
     ```markdown
     <div style="text-align: center;">
       <i class="fas fa-brain fa-2x"></i>
     </div>
     ```
   - Multiple icons:
     ```markdown
     <div style="text-align: center;">
       <i class="fas fa-brain fa-2x" style="margin-right: 20px;"></i>
       <i class="fas fa-arrow-right fa-2x"></i>
       <i class="fas fa-running fa-2x" style="margin-left: 20px;"></i>
     </div>
     ```

## Mini-Lecture Implementation

### Breaking Down Presentations

For better engagement and clarity, long presentations should be broken down into mini-lectures of approximately 10 minutes each. Follow these guidelines:

1. **File Naming Convention**
   - Base name: Original presentation filename
   - Append `-1`, `-2`, etc. for each part
   - Example: `479-ch01-1_8.qmd` becomes:
     - `479-ch01-1_8-1.qmd`
     - `479-ch01-1_8-2.qmd`
     - etc.

2. **Structure of Each Part**
   - **Review Slide** (Start of each part except first)
     ```markdown
     ## Review and Preview
     
     :::::::::: columns
     ::: {.column width="50%"}
     **Previously Covered:**
     - Key points from previous part
     :::
     
     ::: {.column width="50%"}
     **In This Section:**
     - Topics to be covered
     :::
     ::::::::::
     ```

   - **Content Slides**
     - Maintain consistent formatting
     - Include all original content
     - Preserve audio references
     - Keep speaker notes
     
   - **Transition Slide** (End of each part except last)
     ```markdown
     ## Coming Up Next: [Next Part Title]
     
     :::::::::: columns
     ::: {.column width="60%"}
     In the next part, we'll explore:
     
     - Topic 1
     - Topic 2
     - Topic 3
     
     Brief description of why these topics matter.
     :::
     
     ::: {.column width="40%"}
     ::: {.center}
     <div class="icon-container">
     <i class="fas fa-[relevant-icon] fa-7x"></i>
     </div>
     :::
     :::
     ::::::::::
     ```

3. **Final Part Special Considerations**
   - Replace transition slide with summary
   - Include comprehensive review
   - Add "Looking Ahead" section

4. **Content Distribution**
   - Aim for equal length parts
   - Keep related topics together
   - Ensure logical flow between parts
   - Maintain all original content

5. **Audio Files**
   - Keep original audio file names
   - Ensure audio references match new file structure
   - Update audio paths if needed

6. **Navigation**
   - Each part functions as standalone presentation
   - Maintain consistent styling across parts
   - Use menu for easy navigation between parts

## Flashcards Implementation

### Directory Structure for Flashcards
```
slides/
├── ch01/
│   └── flashcards/
│       ├── 479-ch01-1_8-1-flashcards.qmd  # Part 1 flashcards
│       ├── 479-ch01-1_8-2-flashcards.qmd  # Part 2 flashcards
│       └── ...
```

### Flashcard YAML Configuration
```yaml
---
title: "Chapter X-Y Flashcards"
subtitle: "Topic: Specific Topic"
format:
  revealjs:
    theme: default
    width: 1600
    height: 900
    margin: 0.1
    controls: true
    navigation-mode: linear
    flashcards:
      flipKey: 'q'
      shuffleKey: 't'
      showFlipButton: true
    footer: "Navigation: Press 'q' to flip card | 't' to shuffle | Arrow keys for next/previous"
    slide-number: true
revealjs-plugins:
  - flashcards
editor: source
---
```

### Flashcard Structure
Each flashcard should follow this format:
```markdown
## Term Name {.flashcard}

::: {.flashcard-front}
Term: [The concept or term]
:::

::: {.flashcard-back}
Definition: [Clear, comprehensive definition]
:::
```

## Quiz Implementation

### Directory Structure for Quizzes
```
slides/
├── ch01/
│   └── quizzes/
│       ├── 479-ch01-1_8-1-quiz.qmd  # Part 1 quiz
│       └── ...
```

### Quiz YAML Configuration
```yaml
---
title: "Chapter X-Y Quiz"
subtitle: "Topic: Specific Topic"
format:
  revealjs:
    theme: default
    width: 1600
    height: 900
    margin: 0.1
    controls: true
    navigation-mode: linear
    quiz:
      checkKey: 'c'
      resetKey: 'r'
      shuffleKey: 't'
      allowNumberKeys: true
      disableOnCheck: false
      shuffleOptions: false
      defaultCorrect: "Correct! You understand this concept."
      defaultIncorrect: "Review this concept in your notes."
    footer: "Navigation: Press 'c' to check answer | 'r' to reset | Arrow keys for next/previous"
    slide-number: true
revealjs-plugins:
  - quiz
editor: source
---
```

### Quiz Question Structure
Each quiz question should follow these guidelines:
1. TRUE option always appears first
2. Mix of TRUE and FALSE as correct answers (approximately 50/50)
3. Clear question statement that supports the correct answer
4. Detailed explanations for both options

Example format:
```markdown
## Topic Name {.quiz-question}

[Question statement that makes the TRUE/FALSE answer logical]

- [True]{.correct data-explanation="Detailed explanation why this is correct"}
- [False]{data-explanation="Detailed explanation why this is incorrect"}

# OR

- [True]{data-explanation="Detailed explanation why this is incorrect"}
- [False]{.correct data-explanation="Detailed explanation why this is correct"}
```

### Quiz Design Principles
1. Maintain consistent formatting across all questions
2. Ensure questions test understanding, not just memorization
3. Write clear, unambiguous questions
4. Provide helpful, educational explanations
5. Balance TRUE/FALSE correct answers throughout the quiz
6. Keep TRUE option as the first choice always
7. Disable option shuffling in YAML configuration

## PowerPoint to Quarto Conversion

### Features

- Converts PowerPoint slides to Quarto RevealJS presentation format
- Preserves speaker notes and formats them according to Quarto's documentation
- Automatically extracts and saves images from slides
- Creates two-column layout for slides containing images (65% text, 35% images)
- Uses level 2 headers (##) for slide titles
- Maintains PowerPoint bullet points and text formatting
- Saves output files with the same name as input files (e.g., `lecture.pptx` → `lecture.qmd`)
- if the image is too wide, place it below the bullet points.

### Requirements

- Python 3.x
- python-pptx
- python-slugify

### Setup Instructions

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

### Using the Converter

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

## Audio Implementation

### Audio Generation Details

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

### Audio Implementation Steps

1. Create the audio-player.js file in your chapter's js directory:
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
           autoPlayMedia: true // Enable auto-play for media
       });

       // Listen for slide changes
       Reveal.on('slidechanged', handleSlideTransition);
       
       // Start audio playback for first slide
       handleSlideTransition();
   });
   ```

2. Update your QMD file's YAML header:
   ```yaml
   format: 
     revealjs:
       # Other settings...
       auto-play-media: true
       include-in-header:
         - text: |
             <script src="js/audio-player.js"></script>
   ```

3. Add audio to individual slides:
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

4. Audio Behavior:
   - Audio plays automatically when each slide is shown
   - Slides advance automatically after:
     - Audio finishes playing (plus 1 second delay)
     - 5 seconds if there's no audio
   - You can still use arrow keys or space to manually control slides

5. File Paths:
   - Audio files: Use relative paths from your QMD file (e.g., `../audio/filename.mp3`)
   - JavaScript: Place in `js` directory next to your QMD file
   - Reference paths relative to the QMD file's location

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

## Adding New Chapters

To add a new chapter to the web application, follow these steps:

1. **Create Directory Structure**
   Create a new directory under `slides/` following the naming convention `chXX` (where XX is the two-digit chapter number, e.g., `ch01`, `ch02`):

   ```
   slides/
   ├── chXX/
   │   ├── flashcards/
   │   │   └── part-1.qmd  # Flashcards for part 1
   │   └── quizzes/
   │       └── part-1.qmd  # Quiz for part 1
   ```

2. **Create Flashcard Files**
   In the `flashcards` directory, create `.qmd` files following this format:

   ```markdown
   ---
   title: "Chapter XX Flashcards"
   ---

   Term: [Term Name]
   Definition: [Term Definition]

   Term: [Another Term]
   Definition: [Another Definition]
   ```

3. **Create Quiz Files**
   In the `quizzes` directory, create `.qmd` files following this format:

   ```markdown
   ---
   title: "Chapter XX Quiz"
   ---

   .quiz-question
   [Question Text]
   [Answer Option 1].correct
   [Answer Option 2]

   .quiz-question
   [Another Question]
   [Answer Option 1]
   [Answer Option 2].correct
   ```

4. **File Naming Convention**
   - For flashcards: `part-N.qmd` (where N is the part number)
   - For quizzes: `part-N.qmd` (where N is the part number)

5. **Deploy Changes**
   After adding new content:
   1. Commit your changes to Git
   2. Push to GitHub
   3. Reboot the Streamlit app

The web application will automatically detect and display the new chapter in the dropdown menu.

## Testing

1. **Audio**
   - Verify all audio files exist and paths are correct
   - Test audio playback on each slide
   - Check audio file names match slide content

2. **Images**
   - Verify images display correctly

3. **Layout**
   - Test responsive behavior
   - Verify column alignment
   - Check for any content overflow

## Common Issues and Solutions

1. **Audio 404 Errors**
   - Check file paths are relative (`../audio/`)
   - Verify file names match exactly
   - Ensure audio files exist in correct directory

2. **Layout Problems**
   - Keep YAML margin setting at 0.1
   - Use proper column width settings
   - Maintain consistent structure across slides

3. **Image Generation**
   - Provide detailed, specific prompts
   - Include style specifications
   - Keep prompts consistent with content
