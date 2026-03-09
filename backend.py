import os, pickle
from langchain_community.llms import Ollama
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

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

def init_conversation(topic):
    memory = ConversationBufferMemory()
    loaded_messages = load_conversation(topic)
    for msg in loaded_messages:
        memory.chat_memory.add_message(msg)
    return ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=True)
