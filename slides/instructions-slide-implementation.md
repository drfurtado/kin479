# Slide Implementation Instructions

This document provides instructions for implementing Quarto presentations for the KIN479 course, based on successful implementations.

## Directory Structure

```
slides/
├── ch01/
│   ├── source-files/      # Contains Quarto files
│   │   ├── js/           # JavaScript files
│   │   │   ├── audio-player.js
│   │   │   ├── record-presentation.js
│   │   │   ├── flux-config.js
│   │   │   └── flux-bundle.js
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
      .flux-generated-image {
        max-width: 100%;
      }
      </style>
      <script>
      window.addEventListener('load', function() {
          Reveal.configure({ keyboard: false });
      });
      </script>
      <script src="js/audio-player.js"></script>
      <script src="js/record-presentation.js"></script>
      <script src="js/flux-config.js"></script>
      <script src="js/flux-bundle.js"></script>
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
::: {.flux-container data-prompt="Detailed prompt for image generation"}
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

2. **Image Generation**
   - Use `.flux-container` with detailed prompts
   - Include style specifications in prompts
   - Keep prompts consistent with slide content

3. **Layout**
   - Use two-column layout with 50% width each
   - Left column for bullet points
   - Right column for generated images
   - Keep bullet points concise and clear

4. **Notes**
   - Include detailed speaker notes for each slide
   - Notes should match audio content
   - Use conversational, engaging tone

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
│       ├── 479-ch01-1_8-2-quiz.qmd  # Part 2 quiz
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

## Testing

1. **Audio**
   - Verify all audio files exist and paths are correct
   - Test audio playback on each slide
   - Check audio file names match slide content

2. **Images**
   - Verify flux containers are properly configured
   - Check image generation prompts
   - Ensure images display correctly

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
