import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import tempfile
import os
load_dotenv()
subscription_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_REGION")
azure_subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
st.set_page_config(page_title="Speech to Text", layout="centered")
st.title("🎙️ Speech to Text")

uploaded_file = st.file_uploader("Upload an audio or video file", type=["wav", "mp3", "mp4", "m4a"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_filename = temp_file.name

    # Configure the Azure Speech service
    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key,
        region=region
    )

    audio_config = speechsdk.audio.AudioConfig(filename=temp_filename)

    intent_recognizer = speechsdk.intent.IntentRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    model = speechsdk.intent.LanguageUnderstandingModel(app_id=azure_subscription_id)
    intents = [
        (model, "HomeAutomation.TurnOn"),
        (model, "HomeAutomation.TurnOff")
    ]

    intent_recognizer.add_intents(intents)
    
    st.write("🔍 Recognizing... please wait.")
    result = intent_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        st.success("📝 Recognized Text:")
        st.markdown(f"**{result.text}**")
    else:
        st.error("Speech not recognized. Reason: " + str(result.reason))

    # Clean up the temporary file
    os.remove(temp_filename)
