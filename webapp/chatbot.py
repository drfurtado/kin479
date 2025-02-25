import os
import json
import requests
from typing import List, Dict
from dotenv import load_dotenv

class ChatBot:
    def __init__(self, model_name=None):
        """Initialize chatbot with OpenRouter API"""
        load_dotenv(verbose=True)
        
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        print(f"API key found: {'Yes' if self.api_key else 'No'}")
        
        # Set up OpenRouter API
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://drfurtado.github.io/",
            "X-Title": "KIN377 Study Assistant",
            "Content-Type": "application/json"
        }
        
        # Set model name - only using Gemini Pro
        self.model_name = "google/gemini-2.0-pro-exp-02-05:free"
        print(f"Using model: {self.model_name}")
        
        self.context = {}  # Store content by chapter
        self.conversation_history = []  # Store conversation history
        self.max_history = 5  # Maximum number of past exchanges to keep

    def get_available_models(self):
        """Return the list of available models"""
        return {"Gemini Pro": "google/gemini-2.0-pro-exp-02-05:free"}
        
    def set_model(self, model_name):
        """Set the model to use for chat completions"""
        if model_name == "google/gemini-2.0-pro-exp-02-05:free":
            self.model_name = model_name
            print(f"Switched to model: {model_name}")
            return True
        return False

    def load_all_chapters(self, slides_dir: str) -> None:
        """Load content from all chapters"""
        self.context = {}
        print(f"Loading chapters from: {slides_dir}")
        
        # Get all chapter directories
        chapter_dirs = [d for d in sorted(os.listdir(slides_dir)) 
                       if os.path.isdir(os.path.join(slides_dir, d)) and d.startswith('ch')]
        print(f"Found chapter directories: {chapter_dirs}")
        
        for chapter_dir in chapter_dirs:
            chapter_path = os.path.join(slides_dir, chapter_dir)
            
            # Skip empty directories
            if not any(os.scandir(chapter_path)):
                print(f"Skipping empty directory: {chapter_dir}")
                continue
                
            print(f"Loading content from {chapter_dir}...")
            chapter_content = []
            
            # Load config
            config_file = os.path.join(chapter_path, 'config.json')
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    chapter_content.append(f"Chapter {config.get('chapter_title', '')}: {config.get('chapter_description', '')}")
                    print(f"Loaded config for {chapter_dir}")

            # Load notes
            notes_path = os.path.join(chapter_path, 'notes')
            if os.path.exists(notes_path):
                note_files = [f for f in os.listdir(notes_path) if f.endswith(('.md', '.qmd'))]
                print(f"Found {len(note_files)} note files in {chapter_dir}")
                for file in sorted(note_files):
                    with open(os.path.join(notes_path, file), 'r') as f:
                        content = f.read()
                        if content.strip():
                            chapter_content.append(f"Notes from {file}:\n{content}")

            # Load flashcards
            flashcards_path = os.path.join(chapter_path, 'flashcards')
            if os.path.exists(flashcards_path):
                flashcard_files = [f for f in os.listdir(flashcards_path) if f.endswith(('.md', '.qmd'))]
                print(f"Found {len(flashcard_files)} flashcard files in {chapter_dir}")
                for file in flashcard_files:
                    with open(os.path.join(flashcards_path, file), 'r') as f:
                        content = f.read()
                        if content.strip():
                            chapter_content.append(f"Flashcards from {file}:\n{content}")

            # Load Q&A
            qa_path = os.path.join(chapter_path, 'qa')
            if os.path.exists(qa_path):
                qa_files = [f for f in os.listdir(qa_path) if f.endswith(('.md', '.qmd'))]
                print(f"Found {len(qa_files)} Q&A files in {chapter_dir}")
                for file in qa_files:
                    with open(os.path.join(qa_path, file), 'r') as f:
                        content = f.read()
                        if content.strip():
                            chapter_content.append(f"Q&A from {file}:\n{content}")
            
            # Only add chapter if it has content
            if chapter_content:
                self.context[chapter_dir] = chapter_content
                print(f"Added {len(chapter_content)} content items for {chapter_dir}")
            else:
                print(f"No content found in {chapter_dir}")
        
        total_items = sum(len(content) for content in self.context.values())
        print(f"Finished loading {len(self.context)} chapters with {total_items} total content items")

    def load_chapter_content(self, chapter_path: str, chapter_id: str) -> None:
        """Load content from a specific chapter"""
        chapter_content = []
        print(f"Processing {chapter_id}...")
        
        # Load config
        config_file = os.path.join(chapter_path, 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                chapter_content.append(f"Chapter {config.get('chapter_title', '')}: {config.get('chapter_description', '')}")
                print(f"Loaded config for {chapter_id}")

        # Load notes
        notes_path = os.path.join(chapter_path, 'notes')
        if os.path.exists(notes_path):
            note_files = [f for f in os.listdir(notes_path) if f.endswith(('.md', '.qmd'))]
            print(f"Found {len(note_files)} note files in {chapter_id}")
            for file in sorted(note_files):
                with open(os.path.join(notes_path, file), 'r') as f:
                    content = f.read()
                    if content.strip():
                        chapter_content.append(f"Notes from {file}:\n{content}")

        # Load flashcards - check both in flashcards directory and chapter root
        flashcard_files = []
        
        # Check flashcards subdirectory
        flashcards_path = os.path.join(chapter_path, 'flashcards')
        if os.path.exists(flashcards_path):
            flashcard_files.extend([os.path.join(flashcards_path, f) for f in os.listdir(flashcards_path) 
                                if f.endswith(('.md', '.qmd'))])

        # Check chapter root directory for flashcard files
        root_flashcard_files = [os.path.join(chapter_path, f) for f in os.listdir(chapter_path)
                              if f.lower().endswith(('.md', '.qmd')) and 'fc' in f.lower()]
        flashcard_files.extend(root_flashcard_files)

        if flashcard_files:
            print(f"Found {len(flashcard_files)} flashcard files in {chapter_id}")
            for file_path in flashcard_files:
                with open(file_path, 'r') as f:
                    content = f.read()
                    if content.strip():
                        chapter_content.append(f"Flashcards from {os.path.basename(file_path)}:\n{content}")

        # Load quizzes
        quizzes_path = os.path.join(chapter_path, 'quizzes')
        if os.path.exists(quizzes_path):
            quiz_files = [f for f in os.listdir(quizzes_path) if f.endswith(('.md', '.qmd'))]
            print(f"Found {len(quiz_files)} quiz files in {chapter_id}")
            for file in quiz_files:
                with open(os.path.join(quizzes_path, file), 'r') as f:
                    content = f.read()
                    if content.strip():
                        chapter_content.append(f"Quiz content from {file}:\n{content}")

        # Load Q&A
        qa_path = os.path.join(chapter_path, 'qa')
        if os.path.exists(qa_path):
            qa_files = [f for f in os.listdir(qa_path) if f.endswith(('.md', '.qmd'))]
            print(f"Found {len(qa_files)} Q&A files in {chapter_id}")
            for file in qa_files:
                with open(os.path.join(qa_path, file), 'r') as f:
                    content = f.read()
                    if content.strip():
                        chapter_content.append(f"Q&A content from {file}:\n{content}")
        
        if chapter_content:
            self.context[chapter_id] = chapter_content
            print(f"Successfully loaded {len(chapter_content)} content items for {chapter_id}")
        else:
            print(f"Warning: No content found in {chapter_id}")

    def get_response(self, question: str) -> str:
        """Get a response from the chatbot based on all available content"""
        if not self.api_key:
            return ("Please set up your OpenRouter API key:\n\n"
                   "1. Create an account at https://openrouter.ai\n"
                   "2. Go to https://openrouter.ai/settings/tokens\n"
                   "3. Create a new token with 'read' access\n"
                   "4. Copy the token to the .env file as OPENROUTER_API_KEY")
        
        if not self.context:
            return "No content loaded. Please wait while I load the course materials."
            
        try:
            # Format all available content with chapter information
            formatted_context = ""
            for chapter_id, content_list in self.context.items():
                formatted_context += f"\n=== {chapter_id.upper()} ===\n"
                formatted_context += "\n".join(content_list) + "\n"
            
            # Build conversation messages with instruction to cite chapters
            messages = [
                {
                    "role": "system", 
                    "content": ("You are a KIN377 teaching assistant. Use the provided course content to answer questions. "
                              "When answering, ALWAYS specify which chapter(s) the information comes from. "
                              "When answering, ALWAYS include specific details and examples from the content. "
                              "If information comes from multiple chapters, organize your response by chapter. "
                              "If a question cannot be answered using the provided content, explicitly state that.")
                }
            ]
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Add current context and question
            messages.append({
                "role": "user", 
                "content": f"Using the following course content:\n\n{formatted_context}\n\nQuestion: {question}"
            })

            # Prepare the request payload
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 1000
            }

            print("\nMaking API request...")
            print(f"Model: {self.model_name}")
            print(f"Headers: {json.dumps(self.headers, indent=2)}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            print(f"\nAPI Response:")
            print(f"Status: {response.status_code}")
            print(f"Headers: {json.dumps(dict(response.headers), indent=2)}")
            print(f"Content: {response.text}")
            
            if response.status_code == 200:
                print("\n=== RAW RESPONSE TEXT ===")
                print(response.text)
                print("\n=== END RAW RESPONSE TEXT ===")
                
                try:
                    response_json = response.json()
                    print("\n=== PARSED JSON ===")
                    print(type(response_json))
                    print(response_json)
                    print("\n=== END PARSED JSON ===")
                    
                    # Try to get the response content, printing each step
                    if 'choices' in response_json:
                        print("\nFound 'choices' key")
                        choices = response_json['choices']
                        print(f"Choices: {choices}")
                        
                        if choices and len(choices) > 0:
                            print("\nFound first choice")
                            first_choice = choices[0]
                            print(f"First choice: {first_choice}")
                            
                            if isinstance(first_choice, dict):
                                print("\nFirst choice is a dictionary")
                                if 'message' in first_choice:
                                    print("\nFound 'message' key")
                                    message = first_choice['message']
                                    print(f"Message: {message}")
                                    
                                    if 'content' in message:
                                        print("\nFound 'content' key")
                                        content = message['content']
                                        print(f"Content: {content}")
                                        
                                        # We found the content, use it
                                        response_content = content.strip()
                                        self.conversation_history.append({"role": "user", "content": question})
                                        self.conversation_history.append({"role": "assistant", "content": response_content})
                                        
                                        if len(self.conversation_history) > self.max_history * 2:
                                            self.conversation_history = self.conversation_history[-self.max_history * 2:]
                                        
                                        return response_content
                    
                    # If we get here, we didn't find what we needed
                    print("\nDid not find expected response format")
                    return "I apologize, but I received an unexpected response format. Please try asking your question again."
                    
                except json.JSONDecodeError as e:
                    print(f"\nJSON decode error: {str(e)}")
                    print("Raw text that failed to parse:")
                    print(response.text)
                    return "I apologize, but I encountered an error processing the response. Please try asking your question again."
            elif response.status_code == 401:
                return ("Authentication failed. Please check:\n"
                       "1. Your OpenRouter account is active\n"
                       "2. Your API token is valid\n"
                       "3. Token in .env file is correct")
            elif response.status_code == 429:
                return "Too many requests. Please try again in a few minutes."
            else:
                error_msg = response.text if response.text else str(response.status_code)
                print(f"API error response: {error_msg}")
                return f"I apologize, but I encountered an error ({response.status_code}). Please try asking your question again."
                
        except requests.exceptions.Timeout:
            return "The request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return "I encountered a network error. Please check your connection and try again."
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return "I apologize, but I encountered an unexpected error. Please try asking your question again."