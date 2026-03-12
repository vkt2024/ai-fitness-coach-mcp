import streamlit as st

def setup_ui():
    st.set_page_config(page_title="Fitness AI Assistant", page_icon="🏋️", layout="centered")

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
        align-self: flex-end;
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


def render_chat(chat_history):

    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in chat_history:

        role = msg[0]
        message = msg[1]

        if role == "human":
            bubble = f"""
            <div class="chat-bubble user">
            👤 {message}
            </div>
            """
        else:
            bubble = f"""
            <div class="chat-bubble ai">
            🤖 {message}
            </div>
            """

        st.markdown(bubble, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
