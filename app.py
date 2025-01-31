import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr

# Predefined questions and answers
qa_pairs = {
    "what is my account balance": "Your account balance is fifty thousand rupees.",
    "how can I open a new account": "You can open a new account by providing us with your ID and proof of salary."
}

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

# Function to recognize speech from uploaded audio file
def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error with the speech recognition service."

# Streamlit App
st.title("AI Voice Demo for Bank KIOSK")

st.write("Ask me a question using text or upload a voice recording!")

# Text input option
user_input_text = st.text_input("Type your question here (optional):")

# Voice input option
uploaded_audio = st.file_uploader("Or upload a voice recording (.wav file):", type=["wav"])

# Process user input
if user_input_text or uploaded_audio:
    if uploaded_audio:
        st.write("Processing audio input...")
        user_input = recognize_speech(uploaded_audio)
        st.write(f"You said: {user_input}")
    else:
        user_input = user_input_text.lower()

    # Get the response
    response = qa_pairs.get(user_input, "Sorry, I don't have an answer for that.")
    st.write(f"AI: {response}")

    # Convert the response to audio
    audio_file = text_to_speech(response)
    st.audio(audio_file, format="audio/mp3")

