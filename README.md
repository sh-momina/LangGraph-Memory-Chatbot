# 🧠 LangGraph Memory Chatbot

An advanced **LangGraph-based AI Chatbot** with **persistent memory**, **streaming responses**, and **multi-threaded conversations**, all wrapped in a clean **Streamlit interface**.  

Just like ChatGPT — it remembers previous chats, stores them in a database, and allows you to continue past threads seamlessly.

---

## 🌟 Key Features

✅ **LangGraph-powered architecture** – Uses LangGraph to manage conversation flow and agent logic.  
✅ **Memory & Persistence** – Stores all chat history in a local database for continuous context.  
✅ **Streaming Responses** – See the model’s answer appear in real-time.  
✅ **Multi-threaded Chat Sessions** – Create, switch, and continue different chat threads (like ChatGPT).  
✅ **Tool Integration** – Can be extended with tools or APIs for enhanced functionality.  
✅ **Beautiful Streamlit UI** – Simple and interactive chat interface.

---

## 🧩 Tech Stack

| Component | Description |
|------------|-------------|
| **LangGraph** | Manages the chatbot logic and memory graph |
| **OpenAI API** | Provides the language model (LLM) for responses |
| **SQLite / DB** | Stores chats and memory persistently |
| **Streamlit** | Front-end UI for chatting |
| **Python 3.11** | Core language for the project |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sh-momina/LangGraph-Memory-Chatbot.git
cd LangGraph-Memory-Chatbot
final -> streamlit run ui_db.py
