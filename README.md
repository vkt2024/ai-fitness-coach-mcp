## License

This project is licensed under the MIT License.  
If you use this project, please give proper credit.


# AI Fitness Coach (Local LLM + MCP Tools)

An AI-powered fitness assistant built with **LangGraph**, **Ollama**, and **MCP tools**.

This project demonstrates how to build a **local AI agent that can call tools**, retrieve nutrition data, and maintain conversation memory.

---

## Features

• Local LLM using Ollama (Llama 3.1)  
• LangGraph ReAct Agent  
• MCP Tool Integration  
• Nutrition lookup using OpenFoodFacts API  
• Persistent conversation memory  
• User profile memory  
• Streamlit web interface  

---

## Architecture

User → Streamlit UI → LangGraph Agent → MCP Tool → OpenFoodFacts API

---

## Tech Stack

Python  
Streamlit  
LangChain  
LangGraph  
Ollama  
Llama 3.1 (8B)  
MCP (Model Context Protocol)  
OpenFoodFacts API  

---

## Installation

### 1 Install Ollama
Install Ollama and pull the model first:

ollama pull llama3.1:8b

https://ollama.ai

Pull model:
ollama pull llama3.1:8b


---

### 2 Clone Repository
git clone https://github.com/yourusername/ai-fitness-coach-mcp.git

cd ai-fitness-coach-mcp


---

### 3 Create Virtual Environment
python -m venv .venv

Activate:
Windows
.venv\Scripts\activate

---

### 4 Install Dependencies
pip install -r requirements.txt


---

### 5 Start MCP Server
python mcp_server.py

---

### 6 Run App
streamlit run updated_main.py



---

## Example Questions

• "How can I reduce belly fat?"  
• "Nutrition of 2 eggs?"  
• "Healthy breakfast ideas?"

---

## Learning Goals

This project demonstrates:

• AI agents with LangGraph  
• Tool calling with MCP  
• Local LLM applications  
• Persistent memory systems  

---

## Future Improvements

• Vector database memory  
• Automatic body stat extraction  
• Workout plan generation  
• Meal planning system  
• Voice assistant support  

---

## Author

Built by Vivek Tyagi


