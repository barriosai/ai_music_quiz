from openai import OpenAI
import streamlit as st
import openai
import random

# Function to retrieve the API key
def get_api_key():
    return st.secrets["api_key"]

# Initialize OpenAI client
api_key = get_api_key()
openai.api_key = api_key


# Define all major triads
major_triads = {
    'C': ['C', 'E', 'G'],
    'C#': ['C#', 'E#', 'G#'],
    'Db': ['Db', 'F', 'Ab'],
    'D': ['D', 'F#', 'A'],
    'D#': ['D#', 'Fx', 'A#'],
    'Eb': ['Eb', 'G', 'Bb'],
    'E': ['E', 'G#', 'B'],
    'F': ['F', 'A', 'C'],
    'F#': ['F#', 'A#', 'C#'],
    'Gb': ['Gb', 'Bb', 'Db'],
    'G': ['G', 'B', 'D'],
    'G#': ['G#', 'B#', 'D#'],
    'Ab': ['Ab', 'C', 'Eb'],
    'A': ['A', 'C#', 'E'],
    'A#': ['A#', 'Cx', 'E#'],
    'Bb': ['Bb', 'D', 'F'],
    'B': ['B', 'D#', 'F#']
}

def get_hint(triad):
    completion = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
       {"role": "system", "content": "You are a music teacher, skilled in explaining music theory and programming with a creative flair."},
       {"role": "user", "content": f"Can you give me a hint for identifying the notes in the {triad} major triad? Don't give it away just help with a good educational hint. Just give the hint, don't reply with Certainly, just the hint."}
])

    return completion.choices[0].message.content.strip()

def quiz_major_triads_with_hints():
    st.title("Major Triads Quiz with AI Hints")
    st.write("You will be asked to enter the notes in various major triads.")
    st.write("Please enter the notes separated by commas and spaces (e.g., C, E, G).")

    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_key' not in st.session_state:
        st.session_state.current_key = random.choice(list(major_triads.keys()))
    if 'continue_quiz' not in st.session_state:
        st.session_state.continue_quiz = True

    if st.session_state.continue_quiz:
        current_key = st.session_state.current_key
        hint = get_hint(current_key)
        st.write(f"Hint: {hint}")
        
        answer = st.text_input(f"What are the notes in the {current_key} major triad?", key="answer")
        
        if st.button("Submit Answer"):
            answer_list = [note.strip() for note in answer.split(',')]
            if answer_list == major_triads[current_key]:
                st.write("Correct!")
                st.session_state.correct_answers += 1
            else:
                correct_order = ', '.join(major_triads[current_key])
                st.write(f"Incorrect. The correct notes are {correct_order}")

            st.session_state.total_questions += 1
            st.session_state.current_key = random.choice(list(major_triads.keys()))
            st.experimental_rerun()

        if st.button("End Quiz"):
            st.session_state.continue_quiz = False
            st.write(f"\nYou got {st.session_state.correct_answers} out of {st.session_state.total_questions} correct.")
            st.session_state.correct_answers = 0
            st.session_state.total_questions = 0

# Start the quiz
quiz_major_triads_with_hints()
