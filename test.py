import pyttsx3
from langchain_community.llms import Ollama


llm = Ollama(model="llama3:8b")

engine = pyttsx3.init()

def speak(text: str):
    if not isinstance(text, str):
        text = str(text)   # ensure string
    engine.say(text)
    engine.runAndWait()

def ask_llm(user_query):
    result = llm.invoke(user_query)
    print(result)
    return result

speak(ask_llm("Hi"))
