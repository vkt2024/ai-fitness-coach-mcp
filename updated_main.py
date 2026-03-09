import streamlit as st
import os
from new_backend import init_conversation, save_conversation, list_topics, load_conversation
from frontend import setup_ui
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

setup_ui()

# ---------------- SESSION INIT ---------------- #

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔥 Load previous chat if topic already exists
if "topic" in st.session_state and st.session_state.topic:
    if not st.session_state.chat_history:
        st.session_state.chat_history = load_conversation(st.session_state.topic)


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📂 Chat Topics")
topics = list_topics()
active_topic = st.session_state.get("topic")

for t in topics:
    col1, col2 = st.sidebar.columns([4, 1])

    with col1:
        if active_topic == t:
            st.markdown(f"**➡️ {t}**")
        else:
            if st.sidebar.button(t, key=f"topic_{t}"):
                st.session_state["topic"] = t
                st.session_state.conversation = init_conversation(t)
                st.session_state.chat_history = load_conversation(t)

    with col2:
        if st.sidebar.button("🗑️", key=f"delete_{t}"):
            if os.path.exists(f"{t}.pkl"):
                os.remove(f"{t}.pkl")
            st.sidebar.success(f"Deleted '{t}'")

# New topic
new_topic = st.sidebar.text_input("➕ Start new chat (topic name):", key="new_topic")
if new_topic and st.sidebar.button("Create Chat"):
    st.session_state["topic"] = new_topic
    st.session_state.conversation = init_conversation(new_topic)
    st.session_state.chat_history = []


# ---------------- MAIN OPTIONS ---------------- #

option = st.selectbox("Choose an option", ["Ask Fitness Question", "Check your BMI"])


# ===================================================
#  FITNESS CHAT (NOW MCP ENABLED)
# ===================================================

if option == "Ask Fitness Question":

    st.subheader("💬 Conversational Fitness Chatbot")

    topic = st.session_state.get("topic")

    if topic:

        if st.session_state.conversation is None:
            st.session_state.conversation = init_conversation(topic)

        user_text = st.text_input("Enter your question:", key="user_input")
        submit_text = st.button("Ask")

        if submit_text and user_text.strip():

            logging.info(f"User asked (topic={topic}): {user_text.strip()}")

            try:
                # 🔥 THIS IS THE MCP-READY CHANGE
                result = st.session_state.conversation.invoke(
                    {"messages": [{"role": "user", "content": user_text.strip()}]}
                )

                response = result["messages"][-1].content if result.get("messages") else "No response"

                logging.info(f"AI response: {response[:100]}...")

                # Save to session history
                st.session_state.chat_history.append(("human", user_text.strip()))
                st.session_state.chat_history.append(("ai", response))

                st.markdown(f"**🤖 Coach:** {response}")

                # Save to file
                save_conversation(st.session_state.chat_history, topic)

            except Exception as e:
                import traceback
                logging.error(traceback.format_exc())
                st.error(f"Error: {str(e)}")

        # Show Chat History
        if st.session_state.chat_history:

            st.subheader(f"💬 Conversation History ({topic})")

            for item in st.session_state.chat_history:

                if isinstance(item, tuple) and len(item) == 2:
                    role, message = item
                else:
                    continue

                if role == "human":
                    st.markdown(f"**👤 You:** {message}")
                else:
                    st.markdown(f"**🤖 Coach:** {message}")
        # Reset
        if st.button("🔄 Reset Chat"):
            st.session_state.chat_history = []
            if os.path.exists(f"{topic}.pkl"):
                os.remove(f"{topic}.pkl")
            st.success(f"Chat history for '{topic}' cleared!")

        # End Chat
        if st.button("⏹ End Chat"):
            st.session_state.chat_history = []
            st.success("Chat ended. Start fresh anytime!")


# ===================================================
#  BMI (NO CHANGE)
# ===================================================

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
            st.error("You are in the obese range. Consult a healthcare professional.")
