import streamlit as st
import os
import glob
import re
import random

# Set page config
st.set_page_config(
    page_title="KIN479 Study Materials",
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
    
    for line in content.split('\n'):
        if 'Term:' in line:
            if current_term and current_definition:
                flashcards.append({"term": current_term, "definition": current_definition})
            current_term = line.split('Term:')[-1].strip()
            current_definition = None
        elif 'Definition:' in line:
            current_definition = line.split('Definition:')[-1].strip()
    
    if current_term and current_definition:
        flashcards.append({"term": current_term, "definition": current_definition})
    
    return flashcards

def parse_quiz_content(content):
    """Extract quiz questions from Quarto markdown content."""
    questions = []
    current_question = None
    current_options = []
    current_correct = None
    
    for line in content.split('\n'):
        if '.quiz-question' in line:
            if current_question:
                questions.append({
                    "question": current_question,
                    "options": current_options,
                    "correct": current_correct
                })
            current_question = ""
            current_options = []
            current_correct = None
        elif current_question is not None:
            if line.strip() and not line.startswith('#') and not '.quiz-question' in line:
                if '[True]' in line or '[False]' in line:
                    option = "True" if '[True]' in line else "False"
                    is_correct = '.correct' in line
                    current_options.append(option)
                    if is_correct:
                        current_correct = option
                elif line.strip() and not '{' in line and not '}' in line:
                    current_question = line.strip()
    
    if current_question:
        questions.append({
            "question": current_question,
            "options": current_options,
            "correct": current_correct
        })
    
    return questions

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
    """Display interactive quiz."""
    if not questions:
        st.warning("No quiz questions found in this section.")
        return

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.show_explanation = False

    current = st.session_state.current_question
    question = questions[current]

    st.write(f"### Question {current + 1} of {len(questions)}")
    st.write(question['question'])

    for option in ['True', 'False']:
        if option not in st.session_state.answers.get(current, {}):
            if st.button(option, key=f"option_{option}"):
                st.session_state.answers[current] = {
                    'selected': option,
                    'correct': option == question['correct']
                }
                st.session_state.show_explanation = True
                st.rerun()

    if current in st.session_state.answers:
        answer = st.session_state.answers[current]
        if answer['correct']:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect. The correct answer is: " + question['correct'])

    col1, col2 = st.columns(2)
    with col1:
        if current > 0 and st.button("⬅️ Previous Question"):
            st.session_state.current_question -= 1
            st.session_state.show_explanation = False
            st.rerun()
    with col2:
        if current < len(questions) - 1 and st.button("Next Question ➡️"):
            st.session_state.current_question += 1
            st.session_state.show_explanation = False
            st.rerun()

def main():
    st.title("KIN479 Study Materials")
    
    # Initialize session state
    if 'card_flipped' not in st.session_state:
        st.session_state.card_flipped = False
    
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'slides')
    chapters = sorted([d for d in os.listdir(base_path) if d.startswith('ch') and os.path.isdir(os.path.join(base_path, d))])
    
    if not chapters:
        st.error("No chapters found!")
        return
    
    # Chapter selection
    chapter = st.selectbox("Select Chapter", chapters)
    chapter_path = os.path.join(base_path, chapter)
    
    # Mode selection
    mode = st.radio("Select Mode", ["Flashcards", "Quiz"])
    
    if mode == "Flashcards":
        flashcards_path = os.path.join(chapter_path, 'flashcards')
        if os.path.exists(flashcards_path):
            parts = sorted([f for f in os.listdir(flashcards_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                content = load_content(os.path.join(flashcards_path, part))
                flashcards = parse_flashcard_content(content)
                display_flashcards(flashcards)
            else:
                st.warning("No flashcards found for this chapter.")
    else:
        quizzes_path = os.path.join(chapter_path, 'quizzes')
        if os.path.exists(quizzes_path):
            parts = sorted([f for f in os.listdir(quizzes_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                content = load_content(os.path.join(quizzes_path, part))
                questions = parse_quiz_content(content)
                display_quiz(questions)
            else:
                st.warning("No quizzes found for this chapter.")

if __name__ == "__main__":
    main()
