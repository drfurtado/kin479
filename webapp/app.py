import streamlit as st
import os
import glob
import re
import random
import base64
import json

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
    
    # Check if this is the new RevealJS quiz format or the old format
    if '{.quiz-question}' in content:
        # New RevealJS quiz format
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and YAML front matter
            if not line or line.startswith('---'):
                i += 1
                continue
                
            # Question starts with ## and {.quiz-question}
            if line.startswith('##') and '{.quiz-question}' in line:
                # Save previous question if exists
                if current_question and current_options:
                    questions.append({
                        "question": current_question,
                        "options": current_options,
                        "correct": current_correct
                    })
                
                # Get the question text from the next line
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                if i < len(lines):
                    current_question = lines[i].strip()
                    current_options = []
                    current_correct = None
                
            # Option line starts with -
            elif line.startswith('-'):
                option_text = line[1:].strip()  # Remove the dash
                
                # Extract the actual option text (remove markdown formatting)
                option = re.sub(r'\[([^\]]+)\].*', r'\1', option_text).strip()
                
                # Check if this is the correct answer
                if '{.correct' in option_text:
                    current_correct = option
                
                current_options.append(option)
                    
            i += 1
    else:
        # Old quiz format
        quiz_section = re.search(r'::: {\.quiz-options}(.*?):::', content, re.DOTALL)
        if quiz_section:
            quiz_content = quiz_section.group(1)
            questions_raw = re.split(r'\d+\.\s+', quiz_content)[1:]  # Split by numbered items
            
            for q_raw in questions_raw:
                lines = q_raw.strip().split('\n')
                if not lines:
                    continue
                    
                question = lines[0].strip()
                options = []
                correct = None
                
                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith('-'):
                        # Extract option text
                        option_match = re.search(r'-\s*\[(x| )\]\s*(.*)', line)
                        if option_match:
                            is_correct = option_match.group(1) == 'x'
                            option_text = option_match.group(2).strip()
                            options.append(option_text)
                            if is_correct:
                                correct = option_text
                
                if question and options:
                    questions.append({
                        "question": question,
                        "options": options,
                        "correct": correct
                    })
    
    # Add the last question for RevealJS format
    if current_question and current_options:
        questions.append({
            "question": current_question,
            "options": current_options,
            "correct": current_correct
        })
    
    return questions

def parse_qa_content(content):
    """Extract Q&A pairs from Quarto markdown content."""
    qa_pairs = []
    current_question = None
    current_answer = None
    
    for line in content.split('\n'):
        if 'Question:' in line:
            if current_question and current_answer:
                qa_pairs.append({"question": current_question, "answer": current_answer})
            current_question = line.split('Question:')[-1].strip()
            current_answer = None
        elif 'Answer:' in line:
            current_answer = line.split('Answer:')[-1].strip()
    
    if current_question and current_answer:
        qa_pairs.append({"question": current_question, "answer": current_answer})
    
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
    """Display interactive quiz."""
    if not questions:
        st.warning("No quiz questions found in this section.")
        return

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.show_explanation = False
        st.session_state.quiz_completed = False

    current = st.session_state.current_question
    question = questions[current]

    # Display progress
    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress)
    
    st.write(f"### Question {current + 1} of {len(questions)}")
    st.write(question['question'])

    # Display options as radio buttons
    selected_option = st.radio(
        "Select your answer:",
        question['options'],
        key=f"question_{current}"
    )

    # Check answer button
    if st.button("Submit Answer", key=f"check_{current}"):
        st.session_state.answers[current] = {
            'selected': selected_option,
            'correct': selected_option == question['correct']
        }
        st.session_state.show_explanation = True
        
        # If this was the last question, mark the quiz as completed
        if len(st.session_state.answers) == len(questions):
            st.session_state.quiz_completed = True
            
        st.rerun()

    # Display result if answer is selected
    if current in st.session_state.answers:
        answer = st.session_state.answers[current]
        if answer['correct']:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. The correct answer is: {question['correct']}")

        # Only show navigation buttons after answering the current question
        col1, col2 = st.columns(2)
        with col1:
            if current > 0 and st.button("⬅️ Previous Question"):
                st.session_state.current_question -= 1
                st.session_state.show_explanation = False
                st.rerun()
        with col2:
            if current < len(questions) - 1:
                # Only allow moving to next question if current question is answered
                if st.button("Next Question ➡️"):
                    st.session_state.current_question += 1
                    st.session_state.show_explanation = False
                    st.rerun()
    else:
        # Show message if question hasn't been answered
        st.info("⚠️ Please submit your answer before moving to the next question.")

    # Display final score when quiz is completed
    if st.session_state.quiz_completed:
        correct_count = sum(1 for a in st.session_state.answers.values() if a['correct'])
        score_percentage = (correct_count/len(questions)*100)
        
        st.markdown("---")
        st.markdown("### 🎉 Quiz Complete!")
        st.markdown(f"#### Your Score: {correct_count}/{len(questions)} ({score_percentage:.1f}%)")
        
        # Add encouraging message based on score
        if score_percentage == 100:
            st.success("🌟 Perfect score! Excellent work!")
        elif score_percentage >= 80:
            st.success("🎯 Great job! You've demonstrated a strong understanding!")
        elif score_percentage >= 60:
            st.info("📚 Good effort! Review the material and try again to improve your score.")
        else:
            st.warning("📖 Keep studying! Review the course materials and try again.")
            
        # Show a summary of incorrect answers
        if score_percentage < 100:
            st.markdown("### Review Incorrect Answers")
            for i, q in enumerate(questions):
                if not st.session_state.answers[i]['correct']:
                    st.markdown(f"""
                    **Question {i + 1}:** {q['question']}  
                    Your answer: {st.session_state.answers[i]['selected']}  
                    Correct answer: {q['correct']}
                    """)
            
        # Add a retry button
        if st.button("Try Quiz Again"):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.show_explanation = False
            st.session_state.quiz_completed = False
            st.rerun()

def display_qa(qa_pairs):
    """Display Q&A pairs interactively."""
    if not qa_pairs:
        st.warning("No Q&A pairs found in this section.")
        return
    
    # Initialize session state for Q&A
    if 'qa_expanded' not in st.session_state:
        st.session_state.qa_expanded = [False] * len(qa_pairs)
    
    st.markdown("### Questions & Answers")
    
    for i, qa in enumerate(qa_pairs):
        # Create an expander for each Q&A pair
        with st.expander(f"Q: {qa['question']}", expanded=st.session_state.qa_expanded[i]):
            st.markdown(f"**A:** {qa['answer']}")
            # Update session state when expander is clicked
            if st.session_state.qa_expanded[i] != st.session_state.get(f'qa_expanded_{i}', False):
                st.session_state.qa_expanded[i] = not st.session_state.qa_expanded[i]

def main():
    st.title("KIN 479 Interactive Learning")
    
    # Get URL parameters
    params = st.experimental_get_query_params()
    selected_chapter = params.get("chapter", [None])[0]
    selected_mode = params.get("mode", [None])[0]
    selected_quiz = params.get("quiz", [None])[0]
    selected_audio = params.get("audio", [None])[0]
    
    st.markdown("""
    Welcome to the KIN 479 Interactive Learning Platform! This web application is designed to help you master the course material through interactive flashcards, quizzes, Q&A, and audio content.
    
    Created by [Ovande Furtado Jr](https://drfurtado.github.io/site/)
    
    The content in this application is based on:  
    Rosenbaum, D. A. (2010). *Human motor control* (2nd ed). Elsevier Inc.
    
    ### How to Use
    1. Select a chapter from the dropdown menu below
    2. Choose between **Flashcards**, **Quiz**, **Q&A**, or **Audio Overview** mode
    3. For Flashcards:
       - Click on a card to flip it and reveal the answer
       - Use the navigation buttons to move between cards
    4. For Quizzes:
       - Answer each question to the best of your ability
       - Submit your answers to see your score and feedback
    5. For Q&A:
       - Click on any question to expand and view its answer
       - Questions are organized by topic for easy reference
    """)
    
    # Initialize session state
    if 'card_flipped' not in st.session_state:
        st.session_state.card_flipped = False
    
    # Get the absolute path to the slides directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.abspath(os.path.join(current_dir, '..', 'slides'))
    
    # Create the base path if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    try:
        chapters = sorted([d for d in os.listdir(base_path) if d.startswith('ch') and os.path.isdir(os.path.join(base_path, d))])
    except Exception as e:
        st.error(f"Error accessing chapters: {str(e)}")
        chapters = []
    
    if not chapters:
        st.warning("No chapters found. Please add chapter directories (e.g., ch01, ch02) in the 'slides' folder.")
        return
    
    # Chapter selection with URL parameter support
    chapter = st.selectbox("Select Chapter", chapters, index=chapters.index(selected_chapter) if selected_chapter in chapters else 0)
    chapter_path = os.path.join(base_path, chapter)
    
    # Display shareable link for chapter
    current_url = f"https://kin479.streamlit.app/?chapter={chapter}"
    col1, col2 = st.columns([3, 1])
    with col1:
        share_url = st.text_input("📎 Share this chapter:", value=current_url, key="share_url", help="Copy this URL to share this chapter's content")
    with col2:
        # Add a copy to clipboard button
        st.write("") # Add a blank space to align the button
        if st.button("📋 Copy", key="copy_url_button"):
            # Use Streamlit's built-in clipboard copy
            st.write(f'<textarea id="copy-text" style="opacity:0;position:absolute;top:-9999px;">{current_url}</textarea>', unsafe_allow_html=True)
            st.write('''
            <script>
            var copyText = document.getElementById("copy-text");
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            </script>
            ''', unsafe_allow_html=True)
            st.toast('URL Copied to Clipboard!', icon='📋')
    
    # Mode selection with URL parameter support
    mode_options = ["Flashcards", "Quiz", "Q&A", "Audio Overview"]
    mode = st.radio("Select Mode", mode_options, index=mode_options.index(selected_mode) if selected_mode in mode_options else 0)
    
    # Update URL parameters
    st.experimental_set_query_params(
        chapter=chapter,
        mode=mode
    )
    
    if mode == "Flashcards":
        flashcards_path = os.path.join(chapter_path, 'flashcards')
        if os.path.exists(flashcards_path):
            parts = sorted([f for f in os.listdir(flashcards_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                # Update URL parameters for flashcards
                st.experimental_set_query_params(
                    chapter=chapter,
                    mode=mode,
                    quiz=part
                )
                content = load_content(os.path.join(flashcards_path, part))
                flashcards = parse_flashcard_content(content)
                display_flashcards(flashcards)
            else:
                st.warning("No flashcards found for this chapter.")
    elif mode == "Audio Overview":
        # First check for audio URL in chapter config
        config_path = os.path.join(chapter_path, 'config.json')
        audio_url = None
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.loads(f.read())
                    audio_url = config.get('audio_overview_url')
            except Exception as e:
                st.error(f"Error reading chapter configuration: {str(e)}")
        
        # If we have a URL, use it
        if audio_url:
            st.audio(audio_url)
            st.markdown(f"*Audio hosted externally*")
        else:
            # Fall back to local file if exists
            audio_path = os.path.join(chapter_path, 'audio')
            audio_file = os.path.join(audio_path, 'overview.mp3')
            if os.path.exists(audio_file):
                st.audio(audio_file)
                st.markdown(f"*Audio hosted locally*")
            else:
                st.info("No audio overview available for this chapter yet.")
        
        # Update URL parameters for audio
        st.experimental_set_query_params(
            chapter=chapter,
            mode=mode
        )
    elif mode == "Q&A":
        qa_path = os.path.join(chapter_path, 'qa')
        if os.path.exists(qa_path):
            parts = sorted([f for f in os.listdir(qa_path) if f.endswith('.qmd')])
            if parts:
                part = st.selectbox("Select Part", parts)
                # Update URL parameters for Q&A
                st.experimental_set_query_params(
                    chapter=chapter,
                    mode=mode,
                    quiz=part
                )
                content = load_content(os.path.join(qa_path, part))
                qa_pairs = parse_qa_content(content)
                display_qa(qa_pairs)
            else:
                st.warning("No Q&A content found for this chapter.")
        else:
            st.warning("No Q&A directory found for this chapter. Please create a 'qa' directory with .qmd files.")
    else:
        quizzes_path = os.path.join(chapter_path, 'quizzes')
        if os.path.exists(quizzes_path):
            parts = sorted([f for f in os.listdir(quizzes_path) if f.endswith('.qmd')])
            if parts:
                # Quiz selection with URL parameter support
                part = st.selectbox("Select Part", parts, index=parts.index(selected_quiz) if selected_quiz in parts else 0)
                # Update URL parameters for quizzes
                st.experimental_set_query_params(
                    chapter=chapter,
                    mode=mode,
                    quiz=part
                )
                content = load_content(os.path.join(quizzes_path, part))
                questions = parse_quiz_content(content)
                display_quiz(questions)
            else:
                st.warning("No quizzes found for this chapter.")

if __name__ == "__main__":
    main()
