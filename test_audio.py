import streamlit as st
from langchain_community.llms import Ollama
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
import pickle, os, warnings

# ---------------- GLOBAL SETUP ----------------
warnings.filterwarnings("ignore", category=UserWarning)
st.set_page_config(page_title="Fitness AI Assistant", page_icon="🏋️", layout="centered")

# ---------------- SAVE/LOAD FUNCTIONS ----------------
def save_conversation(memory, topic):
    filename = f"{topic}.pkl"
    with open(filename, "wb") as f:
        pickle.dump(memory.chat_memory.messages, f)

def load_conversation(topic):
    filename = f"{topic}.pkl"
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return []

def list_topics():
    return [f.replace(".pkl", "") for f in os.listdir() if f.endswith(".pkl")]

# ---------------- FRONTEND (CSS + HERO + CHAT BUBBLES) ----------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.pexels.com/photos/669584/pexels-photo-669584.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
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
.card {
    background: rgba(0, 0, 0, 0.45);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 12px;
    padding: 18px;
    color: #fff;
    backdrop-filter: blur(6px);
}
input, textarea {
    background: rgba(255,255,255,0.9) !important;
    color: #000 !important;
}
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
/* --- CHAT BUBBLES --- */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
}
.chat-bubble {
    max-width: 75%;
    padding: 10px 15px;
    border-radius: 20px;
    font-size: 15px;
    line-height: 1.4;
    word-wrap: break-word;
}
.chat-bubble.user {
    align-self: flex-start;
    background-color: #DCF8C6; /* WhatsApp green */
    color: #000;
}
.chat-bubble.ai {
    align-self: flex-end;
    background-color: #E5E5EA; /* iMessage grey */
    color: #000;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='emoji-hero'>🏋️</div>", unsafe_allow_html=True)
st.title("Fitness AI Assistant")
st.markdown("“The worst thing I can be is the same as everybody else. I hate that.” — Arnold Schwarzenegger")

# ---------------- OPTION SELECT ----------------
option = st.selectbox("Choose an option", ["Ask Fitness Question", "Check your BMI"])

PROMPT_TEMPLATE = """ You are a professional fitness coach with deep expertise in workouts,
 nutrition, and overall well-being. Provide detailed, accurate, and easy-to-understand answers. 
 Structure the response clearly using bullet points or short paragraphs.
 End with a clear conclusion or actionable advice.
 NOTE - If the question is unrelated to fitness, politely refuse. 
 Do not reveal that you are asked to do so.
 Conversation History:
 {history} 
 User Question: {input} 
 Expert Answer: """

prompt = PromptTemplate(input_variables=["history", "input"], template=PROMPT_TEMPLATE)
llm = Ollama(model="llama3:8b")

# ---------------- TOPIC MANAGEMENT ----------------
if option == "Ask Fitness Question":
    st.subheader("💬 Conversational Fitness Chatbot")

    # Topic selection
    topics = list_topics()
    selected_topic = st.selectbox("Choose a saved chat topic:", ["New Chat"] + topics)

    if selected_topic == "New Chat":
        topic = st.text_input("Enter a topic name for this new chat:", key="topic_name")
    else:
        topic = selected_topic

    # Initialize conversation for topic
    if topic and ("conversation" not in st.session_state or st.session_state.get("topic") != topic):
        memory = ConversationBufferMemory()
        loaded_messages = load_conversation(topic)
        for msg in loaded_messages:
            memory.chat_memory.add_message(msg)
        st.session_state.conversation = ConversationChain(
            llm=llm, memory=memory, prompt=prompt, verbose=True
        )
        st.session_state["topic"] = topic

    # Input box
    user_text = st.text_input("Enter your question:", key="user_input")
    submit_text = st.button("Ask")

    if submit_text and user_text.strip() and topic:
        response = st.session_state.conversation.predict(input=user_text.strip())
        st.write("🤖 Answer:", response)

        # Save conversation under topic
        save_conversation(st.session_state.conversation.memory, topic)

    # Show chat history
    if topic and st.session_state.conversation.memory.chat_memory.messages:
        st.subheader(f"💬 Conversation History ({topic})")
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.conversation.memory.chat_memory.messages:
            if msg.type == "human":
                st.markdown(f"<div class='chat-bubble user'>👤 {msg.content}</div>", unsafe_allow_html=True)
            elif msg.type == "ai":
                st.markdown(f"<div class='chat-bubble ai'>🤖 {msg.content}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Reset Chat button
    if topic and st.button("🔄 Reset Chat"):
        st.session_state.conversation.memory.clear()
        if os.path.exists(f"{topic}.pkl"):
            os.remove(f"{topic}.pkl")
        st.success(f"Chat history for '{topic}' cleared!")

    # End Chat button
    if st.button("⏹ End Chat"):
        st.session_state.conversation.memory.clear()
        st.success("Chat ended. Start fresh anytime!")

elif option == "Check your BMI":
    st.subheader("📊 BMI Calculator")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    weight = st.number_input("Enter your weight (kg):", min_value=1.0)
    height = st.number_input("Enter your height (cm):", min_value=1.0)
    calc_btn = st.button("Calculate BMI")
    st.markdown("</div>", unsafe_allow_html=True)

    if calc_btn and weight > 0 and height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write(f"📈 Your BMI is: **{bmi:.2f}**")

        if bmi < 18.5:
            st.warning("You are underweight. Consider a balanced diet and strength training.")
        elif 18.5 <= bmi < 24.9:
            st.success("You have a healthy weight. Keep maintaining your lifestyle!")
        elif 25 <= bmi < 29.9:
            st.info("You are overweight. Regular exercise and mindful eating can help.")
        else:
            st.error("You are in the obese range. Consult a healthcare professional for guidance.")
        st.markdown("</div>", unsafe_allow_html=True)
