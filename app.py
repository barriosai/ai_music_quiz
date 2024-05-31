# app.py
from openai import OpenAI
import streamlit as st
import openai
import time


# Function to retrieve the API key
def get_api_key():
    return st.secrets["api_key"]

# Initialize OpenAI client
api_key = get_api_key()
openai.api_key = api_key


# Function to get a GPT response
client = OpenAI(api_key=st.secrets["api_key"])
def get_gpt_response(question):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a magic 8-ball. Respond to questions with brief, concise spooky and mean answers."},
            {"role": "user", "content": question}
        ]
    )
    return completion.choices[0].message.content.strip()



# Streamlit app
st.title("🔮 Magic 8-Ball")

# Ask the user to enter a question
question = st.text_input("Ask the Magic 8-Ball a question:")

# Placeholder for the response
response_placeholder = st.empty()

# Display button with 8-Ball emoji
if st.button("🎱 Click the 8-Ball to get your answer!"):
    if question.strip() == "":
        st.warning("Please ask a question before clicking the 8-Ball.")
    else:
        with st.spinner("The Magic 8-Ball is thinking..."):
            time.sleep(2)  # Simulate thinking time
            try:
                answer = get_gpt_response(question)
                response_placeholder.markdown(f"<div style='font-size:24px; text-align:center;'>{answer}</div>", unsafe_allow_html=True)
                time.sleep(5)
                response_placeholder.empty()  # Clear the response after 5 seconds
            except Exception as e:
                st.error(f"An error occurred: {e}")
