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

https://ollama.ai

Pull model:
