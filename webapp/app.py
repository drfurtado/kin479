import streamlit as st
import os
import glob
import re
import random
import base64
import json
from chatbot import ChatBot

# Set page config
st.set_page_config(
    page_title="KIN 479 Study Materials",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .flashcard {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        cursor: pointer;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }
    .flashcard.flipped {
        transform: rotateY(180deg);
    }
    .flashcard-content {
        font-size: 1.2em;
        padding: 20px;
    }
    .quiz-option {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        cursor: pointer;
    }
    .quiz-option:hover {
        background-color: #e0e0e0;
    }
    .correct {
        background-color: #90EE90 !important;
    }
    .incorrect {
        background-color: #FFB6C1 !important;
    }
    </style>
""", unsafe_allow_html=True)

def parse_flashcard_content(content):
    """Extract flashcards from Quarto markdown content."""
    flashcards = []
    current_term = None
    current_definition = None
    
    # Split content into lines for processing
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for old format (Term:/Definition:)
        if 'Term:' in line:
            if current_term and current_definition:
                flashcards.append({"term": current_term, "definition": current_definition})
            current_term = line.split('Term:')[-1].strip()
            current_definition = None
        elif 'Definition:' in line:
            current_definition = line.split('Definition:')[-1].strip()
            
        # Check for new format (.flashcard-front/.flashcard-back)
        elif '{.flashcard}' in line:
            front_content = []
            back_content = []
            
            # Skip to start of front content
            while i < len(lines) and '.flashcard-front' not in lines[i]:
                i += 1
            i += 1
            
            # Collect front content
            while i < len(lines) and ':::' not in lines[i]:
                if lines[i].strip():
                    front_content.append(lines[i].strip())
                i += 1
                
            # Skip to start of back content
            while i < len(lines) and '.flashcard-back' not in lines[i]:
                i += 1
            i += 1
            
            # Collect back content
            while i < len(lines) and ':::' not in lines[i]:
                if lines[i].strip():
                    back_content.append(lines[i].strip())
                i += 1
                
            if front_content and back_content:
                flashcards.append({
                    "term": "\n".join(front_content),
                    "definition": "\n".join(back_content)
                })
        i += 1
    
    # Add the last flashcard if exists
    if current_term and current_definition:
        flashcards.append({"term": current_term, "definition": current_definition})
    
    return flashcards

def parse_quiz(content):
    """Parse quiz content into a list of questions with options and answers."""
    questions = []
    current_question = None
    
    # Split content into lines and clean up
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Start of a new question (starts with ## and ends with {.quiz-question})
        if line.startswith('##') and '{.quiz-question}' in line:
            if current_question:
                questions.append(current_question)
            # Extract question text between ## and {.quiz-question}
            question_text = line[2:line.find('{')].strip()
            # Get the actual question content from the next line
            i += 1
            if i < len(lines):
                question_content = lines[i].strip()
                current_question = {
                    'question': f"{question_text}\n{question_content}",
                    'options': [],
                    'answer': None,
                    'explanations': {}
                }
        
        # Parse options (lines starting with -)
        elif line.startswith('-') and current_question:
            # Extract the option text between [ and ]
            start = line.find('[') + 1
            end = line.find(']')
            if start > 0 and end > start:
                option_text = line[start:end].strip()
                current_question['options'].append(option_text)
                
                # Check if this is the correct answer
                if '.correct' in line:
                    current_question['answer'] = len(current_question['options']) - 1
                
                # Extract explanation if present
                exp_start = line.find('data-explanation="')
                if exp_start > 0:
                    exp_start += len('data-explanation="')
                    exp_end = line.find('"', exp_start)
                    if exp_end > exp_start:
                        explanation = line[exp_start:exp_end]
                        current_question['explanations'][len(current_question['options']) - 1] = explanation
        
        i += 1
    
    # Add the last question
    if current_question:
        questions.append(current_question)
    
    return questions

def parse_qa(content):
    """Parse Q&A content into a list of question/answer pairs."""
    qa_pairs = []
    current_qa = None
    
    # Split content into lines
    lines = [line.strip() for line in content.split('\n')]
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Start of a new Q&A pair
        if line.startswith('Question:'):
            if current_qa:
                qa_pairs.append(current_qa)
            current_qa = {
                'question': line[9:].strip(),
                'answer': ''
            }
            
        # Parse answer
        elif line.startswith('Answer:'):
            if current_qa:
                current_qa['answer'] = line[7:].strip()
        
        i += 1
    
    # Add the last Q&A pair
    if current_qa:
        qa_pairs.append(current_qa)
    
    return qa_pairs

def load_content(file_path):
    """Load content from file."""
    with open(file_path, 'r') as file:
        content = file.read()
        # Extract content between first and last --- markers
        if '---' in content:
            parts = content.split('---')
            if len(parts) >= 3:
                return parts[2]
    return content

def display_flashcards(flashcards):
    """Display interactive flashcards."""
    if not flashcards:
        st.warning("No flashcards found in this section.")
        return

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        current_card = st.session_state.get('current_card', 0)
        card = flashcards[current_card]
        
        # Card navigation
        col_prev, col_flip, col_next = st.columns([1, 2, 1])
        
        with col_prev:
            if st.button("⬅️ Previous"):
                st.session_state.current_card = (current_card - 1) % len(flashcards)
                st.session_state.card_flipped = False
                st.rerun()
        
        with col_flip:
            if st.button("🔄 Flip Card"):
                st.session_state.card_flipped = not st.session_state.get('card_flipped', False)
                st.rerun()
        
        with col_next:
            if st.button("Next ➡️"):
                st.session_state.current_card = (current_card + 1) % len(flashcards)
                st.session_state.card_flipped = False
                st.rerun()
        
        # Display card content
        card_container = st.container()
        with card_container:
            if st.session_state.get('card_flipped', False):
                st.info(f"Definition: {card['definition']}")
            else:
                st.success(f"Term: {card['term']}")
        
        # Card counter
        st.text(f"Card {current_card + 1} of {len(flashcards)}")

def display_quiz(questions):
    """Display an interactive quiz."""
    if not questions:
        st.warning("No questions found in this quiz.")
        return
    
    # Initialize session state for answers, current question, and checked answers
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = [None] * len(questions)
    if 'checked_answers' not in st.session_state:
        st.session_state.checked_answers = [False] * len(questions)
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    # Show progress
    progress = st.progress((st.session_state.current_question + 1) / len(questions))
    st.write(f"Question {st.session_state.current_question + 1} of {len(questions)}")
    
    # Display current question
    question = questions[st.session_state.current_question]
    st.markdown(f"### {question['question']}")
    
    # Display options as radio buttons
    current_answer = st.session_state.quiz_answers[st.session_state.current_question]
    index = current_answer if current_answer is not None and current_answer < len(question['options']) else 0
    
    selected = st.radio(
        "Select your answer:",
        options=question['options'],
        key=f"q{st.session_state.current_question}",
        index=index
    )
    
    # Store answer
    if selected in question['options']:
        st.session_state.quiz_answers[st.session_state.current_question] = question['options'].index(selected)
    
    # Check Answer button
    if st.button("Check Answer"):
        st.session_state.checked_answers[st.session_state.current_question] = True
    
    # Show feedback if answer is checked
    if st.session_state.checked_answers[st.session_state.current_question]:
        current_answer = st.session_state.quiz_answers[st.session_state.current_question]
        if current_answer == question['answer']:
            st.success("✅ Correct!")
        else:
            # Show explanation if available
            explanation = question['explanations'].get(current_answer, "")
            st.error(f"❌ {explanation}")
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        # Show number of correct answers so far
        checked = st.session_state.checked_answers.count(True)
        if checked > 0:
            correct = sum(1 for i, q in enumerate(questions) 
                        if st.session_state.checked_answers[i] 
                        and st.session_state.quiz_answers[i] == q['answer'])
            st.write(f"Score so far: {correct}/{checked}")
    
    with col3:
        if st.session_state.current_question < len(questions) - 1:
            if st.button("Next ➡️"):
                st.session_state.current_question += 1
                st.rerun()
    
    # Reset button
    if st.button("Start Over"):
        st.session_state.quiz_answers = [None] * len(questions)
        st.session_state.checked_answers = [False] * len(questions)
        st.session_state.current_question = 0
        st.rerun()

def display_qa(qa_pairs):
    """Display Q&A content using accordions."""
    if not qa_pairs:
        st.warning("No Q&A content found.")
        return
    
    # Display each Q&A pair as an accordion
    for qa in qa_pairs:
        with st.expander(qa['question']):
            st.write(qa['answer'])

def main():
    st.title("KIN 479 Interactive Learning")
    
    st.markdown("""
    Welcome to the KIN 479 Interactive Learning Platform! This web application is designed to help you master the course material through interactive flashcards, quizzes, Q&A, and a chatbot assistant.
    
    Created by [Dr. Ovande Furtado Jr](https://drfurtado.github.io/)
    
    ### How to Use
    1. Select a chapter from the dropdown menu below
    2. Choose between **Flashcards**, **Quiz**, **Q&A**, or **Chat** mode
    3. For Flashcards:
       - Click "Flip Card" to reveal the answer
       - Use the navigation buttons to move between cards
    4. For Quizzes:
       - Answer each question to the best of your ability
       - Submit your answers to see your score and feedback
    5. For Q&A:
       - Click on any question to expand and view its answer
       - Questions are organized by topic for easy reference
    6. For Chat:
       - Ask questions about the course material
       - Get instant responses from our AI assistant
    """)
    
    # Initialize session state
    if 'card_flipped' not in st.session_state:
        st.session_state.card_flipped = False
    if 'current_chapter' not in st.session_state:
        try:
            available_chapters = [d for d in os.listdir(SLIDES_DIR) 
                                if d.startswith('wk') and d != 'wk01' and os.path.isdir(os.path.join(SLIDES_DIR, d))]
            st.session_state.current_chapter = available_chapters[0] if available_chapters else "wk02"
        except:
            st.session_state.current_chapter = "wk02"
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "Flashcards"
    if 'first_load' not in st.session_state:
        st.session_state.first_load = True
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatBot()
        # Get the absolute path to the slides directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        SLIDES_DIR = os.path.abspath(os.path.join(current_dir, '..', 'slides'))
        st.session_state.chatbot.load_all_chapters(SLIDES_DIR)

    def on_chapter_change():
        # Store the new chapter selection
        st.session_state.current_chapter = st.session_state.chapter_select
        
        # Reset all session states related to content
        for key in list(st.session_state.keys()):
            if key in ['current_card', 'card_flipped', 'quiz_answers', 
                      'checked_answers', 'current_question', 'messages']:
                del st.session_state[key]
        
        # Initialize default states
        st.session_state.card_flipped = False
        st.session_state.messages = []
        
        # Force a complete rerun of the app
        st.rerun()

    def on_mode_change():
        st.session_state.current_mode = st.session_state.mode_select
        st.session_state.first_load = False

    # Get the absolute path to the slides directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    SLIDES_DIR = os.path.abspath(os.path.join(current_dir, '..', 'slides'))
    
    # Get list of chapters
    chapters = sorted([d for d in os.listdir(SLIDES_DIR) 
                     if d.startswith('wk') and d != 'wk01' and os.path.isdir(os.path.join(SLIDES_DIR, d))])
    if not chapters:
        st.error("No chapters found. Please make sure the slides directory contains chapter folders (wk01, wk02, etc.)")
        return
    
    # Chapter selection with callback
    chapter = st.selectbox(
        "Select Chapter",
        chapters,
        index=chapters.index(st.session_state.current_chapter) if st.session_state.current_chapter in chapters else 0,
        key="chapter_select",
        on_change=on_chapter_change
    )

    # Update current chapter immediately on first load
    if 'first_load' not in st.session_state:
        st.session_state.first_load = True
        st.session_state.current_chapter = chapter
        st.rerun()

    # Update current chapter if changed
    if st.session_state.current_chapter != chapter:
        st.session_state.current_chapter = chapter
        st.rerun()
    
    # Get chapter path and check for nested chapters
    chapter_path = os.path.join(SLIDES_DIR, st.session_state.current_chapter)
    nested_chapters = [d for d in os.listdir(chapter_path) 
                      if os.path.isdir(os.path.join(chapter_path, d)) and d.startswith('ch')]
    
    if nested_chapters:
        # If there are nested chapters, let user select which one to view
        selected_chapter = st.selectbox("Select Chapter", sorted(nested_chapters))
        chapter_path = os.path.join(chapter_path, selected_chapter)
    
    # Get chapter title from config.json
    config_path = os.path.join(chapter_path, 'config.json')
    chapter_title = ""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            chapter_title = config.get('chapter_title', '')
    
    # Display chapter title in red
    if chapter_title:
        st.markdown(f'<p style="color: red; font-size: 1.2em;">Studying Chapter: {chapter_title}</p>', unsafe_allow_html=True)
    
    # Display shareable link for chapter
    current_url = f"https://kin479.streamlit.app/?chapter={st.session_state.current_chapter}"
    col1, col2 = st.columns([3, 1])
    with col1:
        share_url = st.text_input("📎 Share this chapter:", value=current_url, key="share_url", help="Copy this URL to share this chapter's content")
    with col2:
        # Add a blank space to align the button
        st.write("") 
        # Use st.components to create a clipboard copy button
        copy_html = f'''
        <button onclick="navigator.clipboard.writeText('{current_url}').then(() => 
            alert('URL Copied to Clipboard!'))">📋 Copy</button>
        '''
        st.components.v1.html(copy_html, height=50)
    
    # Mode selection with callback
    mode_options = ["Flashcards", "Quiz", "Q&A", "Audio Overview", "Chat"]
    st.radio(
        "Select Mode",
        mode_options,
        index=mode_options.index(st.session_state.current_mode) if st.session_state.current_mode in mode_options else 0,
        key="mode_select",
        on_change=on_mode_change,
        horizontal=True
    )
    
    if st.session_state.current_mode == "Flashcards":
        flashcards_path = os.path.join(chapter_path, 'flashcards')
        if os.path.exists(flashcards_path):
            parts = sorted([f for f in os.listdir(flashcards_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                with open(os.path.join(flashcards_path, part), 'r') as f:
                    content = f.read()
                flashcards = parse_flashcard_content(content)
                display_flashcards(flashcards)
            else:
                st.warning("No flashcards found for this chapter.")
        else:
            st.warning("No flashcards directory found for this chapter. Please create a 'flashcards' directory with .qmd files.")
    
    elif st.session_state.current_mode == "Quiz":
        quizzes_path = os.path.join(chapter_path, 'quizzes')
        if os.path.exists(quizzes_path):
            parts = sorted([f for f in os.listdir(quizzes_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                with open(os.path.join(quizzes_path, part), 'r') as f:
                    content = f.read()
                questions = parse_quiz(content)
                display_quiz(questions)
            else:
                st.warning("No quizzes found for this chapter.")
        else:
            st.warning("No quizzes directory found for this chapter. Please create a 'quizzes' directory with .qmd files.")
    
    elif st.session_state.current_mode == "Q&A":
        qa_path = os.path.join(chapter_path, 'qa')
        if os.path.exists(qa_path):
            parts = sorted([f for f in os.listdir(qa_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                with open(os.path.join(qa_path, part), 'r') as f:
                    content = f.read()
                qa_pairs = parse_qa(content)
                display_qa(qa_pairs)
            else:
                st.warning("No Q&A content found for this chapter.")
        else:
            st.warning("No Q&A directory found for this chapter. Please create a 'qa' directory with .qmd files.")
    
    elif st.session_state.current_mode == "Audio Overview":
        # Get audio URL from config.json
        config_path = os.path.join(chapter_path, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                audio_url = config.get('audio_overview_url', '')
                if audio_url:
                    st.write("### Chapter Audio Overview")
                    st.audio(audio_url, format='audio/mp3')
                else:
                    st.warning("No audio overview URL found in config.json")
        else:
            st.warning("No config.json found for this chapter.")
    
    elif st.session_state.current_mode == "Chat":
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Accept user input
        if prompt := st.chat_input("Ask a question about the course material..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Show thinking message
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    response = st.session_state.chatbot.get_response(prompt)
                st.markdown(response)
                
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
