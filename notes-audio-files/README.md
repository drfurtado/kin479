# Notes and Audio Generation System

This directory contains all the necessary files to create slide notes from your Quarto presentations and generate audio files using ElevenLabs API.

## Directory Structure
```
notes-audio-files/
├── README.md
├── generate_audio.py
├── slides/          # Your Quarto presentation files (.qmd)
│   └── chXX/       # Chapter-specific slides
│       └── main-source.md    # Source content for the chapter
├── notes/           # Generated conversational notes from slides
└── audio/          # Generated audio files
```

## Process Overview

1. **Source Content**
   - Create a chapter folder in `slides/` (e.g., `slides/ch01/`)
   - Add `main-source.md` containing the complete chapter content
   - This file serves as the authoritative source for all slide content and notes
   - Use it to ensure accuracy and avoid content hallucination

2. **Slide Content (.qmd files)**
   - Create your slides using Quarto (.qmd files)
   - Base slide content on the `main-source.md` file
   - Place in the appropriate chapter directory
   - Use clear, structured content with headers and bullet points
   - If your slides have speaker notes (using ::: notes), these will be used as a starting point

3. **Create Notes**
   - For each slide section, create a corresponding markdown note
   - IMPORTANT: Always refer to `main-source.md` when writing notes to:
     - Ensure accuracy of content
     - Get detailed explanations
     - Find relevant examples
     - Verify terminology
   - If speaker notes exist in the .qmd file:
     - Use them as a foundation
     - Enhance them using content from main-source.md
     - Make them more conversational
   - If no speaker notes exist:
     - Convert slide content into natural language
     - Add examples and explanations from main-source.md
   - Name format: `XX_slide_section_notes.md`
   - Place in the `notes` directory

4. **Generate Audio**
   - Ensure you have an ElevenLabs API key
   - Update the API key in `generate_audio.py`
   - Run the script to generate audio files:
     ```bash
     python generate_audio.py
     ```
   - Audio files will be created in the `audio` directory

## Example Workflow

### 1. Main Source Content (main-source.md):
```markdown
# Chapter 1: Introduction to Motor Skills

Motor skills are fundamental to human movement. They can be classified into several categories:

1. Fine Motor Skills
   - Definition: Skills requiring precise control of small muscles
   - Examples: Writing, typing, surgical procedures
   - Key characteristics: High precision, small movement amplitude

2. Gross Motor Skills
   - Definition: Skills using large muscle groups
   - Examples: Running, jumping, throwing
   - Key characteristics: Full body coordination, larger movement amplitude
```

### 2. Slide Content (ch01.qmd):
```markdown
# Motor Skill Classifications

## Types of Motor Skills
- Fine Motor Skills
  - Small muscle control
  - High precision
- Gross Motor Skills
  - Large muscle groups
  - Full body movements

::: notes
We'll explore different types of motor skills.
:::
```

### 3. Generated Note (01_motor_skills_notes.md):
```markdown
Let's talk about how we classify different types of motor skills. This classification helps us understand how to teach and improve these skills effectively.

First, let's look at fine motor skills. These are the precise movements we make using our small muscles. Think about when you're writing with a pen or typing on a keyboard - these actions require incredibly precise control. Even surgeons rely heavily on fine motor skills during procedures.

On the other hand, we have gross motor skills, which involve our large muscle groups. These are the kinds of movements you use when running, jumping, or throwing a ball. They require your whole body to work together in a coordinated way.

Understanding these differences is crucial because it affects how we learn and teach these skills. The approaches we use to improve fine motor skills might be quite different from those we use for gross motor skills.
```

Note how the generated note:
- Stays true to the source content
- Adds natural transitions
- Includes examples from the source
- Maintains accuracy while being conversational

## Requirements
- Python 3.x
- `requests` library
- ElevenLabs API key

## Setup
1. Install required Python package:
   ```bash
   pip install requests
   ```
2. Update the API key in `generate_audio.py`
3. Create your chapter structure with main-source.md
4. Create slides and notes based on the source
5. Run the script to generate audio

## Tips
- Always refer to main-source.md when creating notes
- Verify facts and examples against the source
- Enhance with conversational elements while maintaining accuracy
- Use transitional phrases between topics
- Keep the language friendly and accessible
- Break complex concepts into simple explanations
