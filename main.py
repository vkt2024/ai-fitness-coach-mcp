import streamlit as st
import os
from backend import init_conversation, save_conversation, list_topics
from frontend import setup_ui
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # INFO for normal ops, DEBUG for detailed traces
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to file
        logging.StreamHandler()          # Also print to console
    ]
)


setup_ui()


# Sidebar navigation
st.sidebar.title("📂 Chat Topics")
topics = list_topics()
active_topic = st.session_state.get("topic")

# Show each topic with a delete button
for t in topics:
    col1, col2 = st.sidebar.columns([4,1])
    with col1:
        # Highlight active topic
        if active_topic == t:
            st.markdown(f"**➡️ {t}**")  # Bold + arrow for active
        else:
            if st.sidebar.button(t, key=f"topic_{t}"):
                st.session_state["topic"] = t
                st.session_state.conversation = init_conversation(t)
    with col2:
        if st.sidebar.button("🗑️", key=f"delete_{t}"):
            if os.path.exists(f"{t}.pkl"):
                os.remove(f"{t}.pkl")
            if st.session_state.get("topic") == t:
                st.session_state.conversation.memory.clear()
                st.session_state.pop("topic")
            st.sidebar.success(f"Deleted '{t}'")

# New chat option
new_topic = st.sidebar.text_input("➕ Start new chat (topic name):", key="new_topic")
if new_topic and st.sidebar.button("Create Chat"):
    st.session_state["topic"] = new_topic
    st.session_state.conversation = init_conversation(new_topic)

option = st.selectbox("Choose an option", ["Ask Fitness Question", "Check your BMI"])

if option == "Ask Fitness Question":
    st.subheader("💬 Conversational Fitness Chatbot")

    topic = st.session_state.get("topic")

    if topic:
        # Input box
        user_text = st.text_input("Enter your question:", key="user_input")
        submit_text = st.button("Ask")

        if submit_text and user_text.strip():
            logging.info(f"User asked (topic={topic}): {user_text.strip()}")
            try:
                response = st.session_state.conversation.predict(input=user_text.strip())
                logging.info(f"AI response (topic={topic}): {response[:100]}...")

                st.write("🤖 Answer:", response)
                save_conversation(st.session_state.conversation.memory, topic)
            except Exception as e:
                logging.error(f"Error generating response: {e}")
                st.error("Something went wrong. Please try again.")

        # Show chat history
        if st.session_state.conversation.memory.chat_memory.messages:
            st.subheader(f"💬 Conversation History ({topic})")
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state.conversation.memory.chat_memory.messages:
                if msg.type == "human":
                    st.markdown(f"<div class='chat-bubble user'>👤 {msg.content}</div>", unsafe_allow_html=True)
                elif msg.type == "ai":
                    st.markdown(f"<div class='chat-bubble ai'>🤖 {msg.content}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Reset Chat button
        if st.button("🔄 Reset Chat"):
            logging.info(f"Chat reset for topic: {topic}")
            st.session_state.conversation.memory.clear()
            if os.path.exists(f"{topic}.pkl"):
                os.remove(f"{topic}.pkl")
            st.success(f"Chat history for '{topic}' cleared!")
            logging.info(f"Topic deleted: {topic}")

        # End Chat button
        if st.button("⏹ End Chat"):
            st.session_state.conversation.memory.clear()
            st.success("Chat ended. Start fresh anytime!")

elif option == "Check your BMI":
    st.subheader("📊 BMI Calculator")
    weight = st.number_input("Enter your weight (kg):", min_value=1.0)
    height = st.number_input("Enter your height (cm):", min_value=1.0)
    if st.button("Calculate BMI") and weight > 0 and height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.write(f"📈 Your BMI is: **{bmi:.2f}**")
        logging.info(f"BMI calculated: weight={weight}, height={height}, bmi={bmi:.2f}")

        if bmi < 18.5:
            st.warning("You are underweight. Consider a balanced diet and strength training.")
        elif 18.5 <= bmi < 24.9:
            st.success("You have a healthy weight. Keep maintaining your lifestyle!")
        elif 25 <= bmi < 29.9:
            st.info("You are overweight. Regular exercise and mindful eating can help.")
        else:
            st.error("You are in the obese range. Consult a healthcare professional for guidance.")
