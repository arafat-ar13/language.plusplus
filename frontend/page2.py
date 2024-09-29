import streamlit as st
import numpy as np
import tempfile
import os
import base64

from gpt import gpt

from st_audiorec import st_audiorec

import azure.cognitiveservices.speech as speechsdk

# Replace with your own subscription key and service region (e.g., "westus").
SUBSCRIPTION_KEY = st.secrets["SUBSCRIPTION_KEY"]
SERVICE_REGION =  st.secrets["SERVICE_REGION"]

# Set up the speech configuration

def getRating(file_name, lang):

    speech_config = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=SERVICE_REGION)


    # Create a pronunciation assessment configuration
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text="",
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme)

    # Create a recognizer with the given settings
    audio_config = speechsdk.audio.AudioConfig(filename=file_name)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language=lang)

    # Apply the pronunciation assessment configuration to the recognizer
    pronunciation_config.apply_to(recognizer)

    print("Processing the WAV file...")

    # Start the recognition
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
        print("Pronunciation Assessment Result:")
        return (result.text, pronunciation_result.accuracy_score, pronunciation_result.fluency_score)
    else:
        return ("", 0.0, 0.0)
    
def page2():
    # Custom CSS for styling and hiding Streamlit elements
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f6;
            color: #000000;
            margin: 0;
            padding: 0;
        }
        .stApp {
            background-color: #f0f2f6;
        }
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: calc(100vh - 60px);
            padding-top: 60px;
        }
        .content {
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .title {
            font-size: 3em;
            font-weight: 700;
            color: #6a1b9a;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .subtitle {
            font-size: 1.5em;
            font-weight: 300;
            color: #9c27b0;
            margin-bottom: 30px;
        }
        .description {
            font-size: 1.2em;
            color: #333333;
            margin-bottom: 40px;
            line-height: 1.6;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .stButton > button {
            background-color: #6a1b9a;
            color: #ffffff;
            border: none;
            border-radius: 25px;
            padding: 12px 24px;
            font-size: 1.2em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 150px;
        }
        .stButton > button:hover {
            background-color: #9c27b0;
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(156, 39, 176, 0.5);
        }
        /* Hide Streamlit elements */
        #MainMenu, footer, header, .stDeployButton {
            display: none !important;
        }
                
        /* Hide audio controls */
        audio {
            display: none;
        }
        /* Top bar styles */
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background-color: #6a1b9a;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .top-bar-title {
            color: #ffffff;
            font-size: 1.5em;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add the top bar
    st.markdown("""
        <div class="top-bar">
            <div class="top-bar-title">Language++</div>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for recording and language selection
    if "recording" not in st.session_state:
        st.session_state.recording = False
    if "language" not in st.session_state:
        st.session_state.language = None

    st.markdown("<h1 class='title'>Language Practice App</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Improve your pronunciation skills</p>", unsafe_allow_html=True)

    if not st.session_state.recording:
        if st.button("Start Recording", key="start_recording"):
            st.session_state.recording = True

    if st.session_state.recording:
        st.markdown("<h2 class='subtitle'>Select a language:</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='button-container'>", unsafe_allow_html=True)
            col_left, col_right = st.columns(2)
            with col_left:
                if st.button("Spanish", key="spanish_button"):
                    st.session_state.language = "Spanish"
            with col_right:
                if st.button("French", key="french_button"):
                    st.session_state.language = "French"
            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.language:
            st.write(f"You selected {st.session_state.language}.")
            st.markdown("<p class='description'>Please start speaking to record your voice.</p>", unsafe_allow_html=True)
            
            wav_audio_data = st_audiorec()

            if wav_audio_data is not None:
                with st.spinner("Processing audio..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                        tmpfile.write(wav_audio_data)
                        tmpfile.flush()
                        if st.session_state.language == "Spanish":
                            text, accuracy, fluency = getRating(tmpfile.name, "es-ES")
                        elif st.session_state.language == "French":
                            text, accuracy, fluency = getRating(tmpfile.name, "fr-FR")

                        print(text, accuracy, fluency)
                        gpt(st.session_state.language, text, accuracy, fluency)

                st.markdown(f"""
                    <audio controls autoplay>
                        <source src="data:audio/mp3;base64,{base64.b64encode(open("output.mp3", "rb").read()).decode()}" type="audio/mp3">
                    </audio>
                """, unsafe_allow_html=True)



    # File uploader
    # audio_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg", "flac"])
        # Add your audio processing and prediction code here