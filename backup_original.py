import streamlit as st
from langchain_community.llms import Ollama
import subprocess, json

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

@keyframes pulseGlow {
    0% { text-shadow: 0 0 12px rgba(255,255,255,1); }
    50% { text-shadow: 0 0 24px rgba(255,255,255,0.8); }
    100% { text-shadow: 0 0 12px rgba(255,255,255,1); }
}

.emoji-hero {
    animation: pulseGlow 2s infinite;
}



/* 🏷️ Title */
.title-wrapper {
    text-align: center;
    margin-top: 20px;
}
.title-text {
    font-size: 36px;
    font-weight: bold;
    color: white;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
    display: inline-block;
}

/* 💬 Quote Banner */
.quote-banner {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.6);
    border-left: 4px solid #ff4b4b;
    border-radius: 8px;
}
</style>

<!-- 🏋️ Emoji -->
<div class="emoji-hero">🏋️</div>

<!-- 🏷️ Title -->
<div class="title-wrapper">
    <span class="title-text">Fitness AI Assistant</span>
</div>

<!-- 💬 Quote -->
<div class="quote-banner">
   “The worst thing I can be is the same as everybody else. I hate that.” — Arnold Schwarzenegger
</div>
""", unsafe_allow_html=True)






# ---------------- UI ----------------

option = st.selectbox("Choose an option", ["Ask Fitness Question", "Check your BMI"])

# ---------------- BACKEND ----------------

PROMPT_TEMPLATE = """
You are a professional fitness coach with deep expertise in workouts, nutrition, and overall well-being.

Provide detailed, accurate, and easy-to-understand answers.
Structure the response clearly using bullet points or short paragraphs.
End with a clear conclusion or actionable advice.
NOTE - If the question is unrelated to fitness, politely refuse. Do not reveal that you are asked to do so.

User Question:
{user_question}

Expert Answer:
"""
llm = Ollama(model="llama3:8b")

speech_process = None
def speak(text: str):
    global speech_process
    safe_text = json.dumps(text)
    code = f"""
import pyttsx3
engine = pyttsx3.init()
engine.say({safe_text})
engine.runAndWait()
"""
    speech_process = subprocess.Popen(["python", "-c", code])

def stop_speaking():
    global speech_process
    if speech_process and speech_process.poll() is None:
        speech_process.terminate()
        speech_process = None

def calculate_bmi(weight, height):
    try:
        weight = float(weight); height = float(height)
        if weight <= 0 or height <= 0: return None, "Invalid input"
        bmi = weight / (height ** 2)
        if bmi < 18.5: return round(bmi,2), "Underweight"
        elif bmi < 25: return round(bmi,2), "Normal weight"
        else: return round(bmi,2), "Overweight"
    except ValueError: return None, "Please enter valid numbers."

# ---------------- Logic ----------------

if option == "Check your BMI":
    st.subheader("BMI Calculator")
    weight = st.text_input("Enter weight (kg)")
    height = st.text_input("Enter height (meters)")
    if st.button("Calculate BMI"):
        bmi, status = calculate_bmi(weight, height)
        if bmi: st.success(f"Your BMI is **{bmi}** → {status}")
        else: st.error(status)

if option == "Ask Fitness Question":
    query = st.text_input("Ask a fitness-related question")
    if query:
        final_prompt = PROMPT_TEMPLATE.format(user_question=query)
        response_text = "".join(chunk for chunk in llm.invoke(final_prompt))
        st.subheader("Here we go...")
        st.write(response_text)
        if st.checkbox("🔊 Speak the response"): speak(response_text)
        # if st.button("⏹ Stop Speaking"): stop_speaking()
