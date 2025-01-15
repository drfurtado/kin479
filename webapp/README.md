# KIN479 Study Materials Web App

A simple, mobile-friendly web application for accessing KIN479 flashcards and quizzes.

## Features

- Access to all chapter flashcards and quizzes
- Mobile-responsive design
- Easy navigation between chapters and sections
- Interactive expandable sections
- Clean, intuitive interface

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Access the application:
- Local: http://localhost:8501
- Network: http://[your-ip]:8501

## Usage

1. Navigate to the desired chapter
2. Choose between Flashcards or Quizzes
3. Click on the expandable sections to view content
4. Use the navigation at the top to move between chapters

## Structure

The application automatically detects and organizes content from the following directory structure:
```
slides/
├── ch01/
│   ├── flashcards/
│   │   └── *.qmd
│   └── quizzes/
│       └── *.qmd
└── ch02/
    ├── flashcards/
    │   └── *.qmd
    └── quizzes/
        └── *.qmd
```

## Development

- Built with Streamlit
- Uses markdown parsing for content display
- Automatically detects new chapters and content
- Mobile-responsive design
