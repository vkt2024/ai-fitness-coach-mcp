import streamlit as st
from langchain_community.llms import Ollama
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
import warnings
from langchain_core.prompts import PromptTemplate

# ---------------- GLOBAL SETUP ----------------
warnings.filterwarnings("ignore", category=UserWarning)

st.set_page_config(page_title="Fitness AI Assistant", page_icon="🏋️", layout="centered")

# ---------------- FRONTEND (CSS + HERO) ----------------
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

# ---------------- MEMORY + CONVERSATION ----------------
if "conversation" not in st.session_state:
    memory = ConversationBufferMemory()
    st.session_state.conversation = ConversationChain(
        llm=llm, memory=memory, prompt=prompt, verbose=True
    )

# ---------------- LOGIC ----------------
if option == "Ask Fitness Question":
    st.subheader("💬 Conversational Fitness Chatbot")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # Clear input before rendering if flagged
    if st.session_state.get("clear_trigger"):
        st.session_state["clear_trigger"] = False
        st.session_state["user_input"] = ""

    # Input box
    user_text = st.text_input("Enter your question:", key="user_input")
    submit_text = st.button("Ask")

    if submit_text and user_text.strip():
        response = st.session_state.conversation.predict(input=user_text.strip())

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🤖 Answer:", response)
        st.markdown("</div>", unsafe_allow_html=True)

        # Set flag to clear on next rerun
        st.session_state["clear_trigger"] = True

    # Show chat history
    if st.session_state.conversation.memory.chat_memory.messages:
        st.subheader("💬 Conversation History")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for msg in st.session_state.conversation.memory.chat_memory.messages:
            if msg.type == "human":
                st.write(f"👤 You: {msg.content}")
            elif msg.type == "ai":
                st.write(f"🤖 Assistant: {msg.content}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Reset Chat button
    if st.button("🔄 Reset Chat"):
        st.session_state.conversation.memory.clear()
        st.session_state.conversation = ConversationChain(
            llm=llm, memory=ConversationBufferMemory(), prompt=prompt, verbose=True
        )
        st.success("Chat history cleared!")

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
