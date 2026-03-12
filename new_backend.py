import os
import pickle
from typing import List, Tuple
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from mcp_adapter import call_mcp_tool_sync


#  LLM

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)


prompt="""
You are a friendly and knowledgeable fitness coach.

Your job is to help users with:
- fat loss
- workouts
- nutrition
- healthy habits

Rules:

- Speak naturally like a human coach, not a robot.
- Do not provide wrong information,if you dont know the answer, you should say i dont know politely.
- Never say things like "based on tool call response".
- Never mention APIs, tools, or MCP.
- If nutrition data is returned by a tool, explain it naturally.
- Give practical and motivating advice.
- Use bullet points for plans.
- Avoid saying "the tool couldn't find".
- Give actionable steps.
- Give actionable steps.

Example style:

User: How can I reduce belly fat?

Coach:
Reducing belly fat comes down to a few simple habits. Focus on eating more protein-rich foods like eggs, fish, chicken, or lentils, because protein helps control hunger and supports muscle.

Combine that with regular activity like brisk walking, running, or strength training for about 30–40 minutes a day.

Also try to reduce sugary drinks and highly processed foods. Small consistent habits make the 
biggest difference."""


# =====================================================
# 2️⃣ MCP TOOL WRAPPER
# =====================================================

@tool
def get_nutrition(food: str) -> str:
    """Fetch nutrition data using MCP server"""
    return call_mcp_tool_sync("get_nutrition", {"food": food})


tools = [get_nutrition]

# =====================================================
# 3️⃣ MEMORY
# =====================================================

memory = MemorySaver()

# =====================================================
# 4️⃣ AGENT
# =====================================================

agent = create_react_agent(
    llm,
    tools,
    checkpointer=memory,
    prompt= prompt
)

# =====================================================
# 5️⃣ INIT CONVERSATION
# =====================================================

# =====================================================
# USER PROFILE MEMORY
# =====================================================

PROFILE_FILE = "user_profile.pkl"

def save_profile(data):
    with open(PROFILE_FILE, "wb") as f:
        pickle.dump(data, f)

def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def init_conversation(topic: str):
    profile = load_profile() or {}

    if not profile:
        save_profile(profile)   # create file if it doesn't exist

    config = {
        "configurable": {"thread_id": topic},
        "profile": profile
    }

    return agent.with_config(config)


# =====================================================
# 6️⃣ SAVE CONVERSATION
# =====================================================

def save_conversation(chat_history: List[Tuple[str, str]], topic: str):
    filename = f"{topic}.pkl"
    with open(filename, "wb") as f:
        pickle.dump(chat_history, f)


# =====================================================
# 7️⃣ LOAD CONVERSATION
# =====================================================

def load_conversation(topic: str):
    filename = f"{topic}.pkl"
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return []


# =====================================================
# 8️⃣ LIST TOPICS
# =====================================================

def list_topics():
    return [
        f.replace(".pkl", "")
        for f in os.listdir()
        if f.endswith(".pkl")
    ]


