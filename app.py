import streamlit as st
from langchain_community.llms import Ollama
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import speech_recognition as sr
import soundfile as sf
import numpy as np

# ---------------- FRONTEND ----------------
st.set_page_config(page_title="Fitness AI Assistant", page_icon="🏋️", layout="centered")

st.markdown("""
<style>
/* 🌄 Background */
.stApp {
    background-image: url("https://images.pexels.com/photos/669584/pexels-photo-669584.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* 🧱 Layout container */
.block-container {
    background: transparent !important;
    padding-top: 0rem !important;
}

.emoji-hero {
    font-size: 64px;
    text-align: center;
    margin-top: 40px;
    margin-bottom: 10px;
    color: #fff;
    text-shadow:
        0 0 12px rgba(255,255,255,1),
        0 0 24px rgba(255,255,255,0.8),
        0 0 36px rgba(255,255,255,0.6);
    filter: drop-shadow(0 0 10px #ffffff);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='emoji-hero'>🏋️</div>", unsafe_allow_html=True)
st.title("Fitness AI Assistant")
st.markdown("“The worst thing I can be is the same as everybody else. I hate that.” — Arnold Schwarzenegger")

# ---------------- TEXT INPUT ----------------
st.subheader("💬 Type your fitness question")
user_text = st.text_input("Enter your question:")
if user_text:
    llm = Ollama(model="llama3:8b")
    response = llm.invoke(user_text)
    st.write("🤖 Answer:", response)

# ---------------- VOICE INPUT ----------------
st.subheader("🎙️ Speak your fitness question")

webrtc_ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=8192,
    media_stream_constraints={"audio": True, "video": False},
)

if webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=5)
    if audio_frames:
        # Concatenate multiple frames into one audio array
        audio_data = np.concatenate([
            f.to_ndarray().flatten().astype(np.int16) for f in audio_frames
        ])
        sample_rate = audio_frames[0].sample_rate

        # Save as proper WAV file
        wav_file = "temp.wav"
        sf.write(wav_file, audio_data, samplerate=sample_rate, format="WAV")

        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_content = recognizer.record(source)
            try:
                spoken_text = recognizer.recognize_google(audio_content)
                st.write(f"🗣️ You said: {spoken_text}")

                # Pass to chatbot
                llm = Ollama(model="llama3:8b")
                response = llm.invoke(spoken_text)
                st.write("🤖 Answer:", response)

            except sr.UnknownValueError:
                st.warning("Could not understand audio")
            except sr.RequestError:
                st.error("Speech recognition service error")
else:
    st.info("🎙️ Please allow microphone access and start speaking.")
