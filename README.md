# 🧠 GitHub Project Analyzer
An **AI-powered local code reviewer** built with **LangChain**, **LangGraph**, and **Ollama**.  
It analyzes repositories, reviews code quality, summarizes commits, and answers natural language questions about your codebase — all **locally**.

---

## 🚀 Features
- 🧩 Understands your repo structure & dependencies  
- 📊 Evaluates code quality, docstrings, and complexity  
- 🧠 Answers natural questions about your code (e.g., “What does this function do?”)  
- 💬 Summarizes git history & recent changes  
- 🔒 100% local — no external API calls required  

---

## ⚙️ Tech Stack
- **LangChain** – reasoning and message orchestration  
- **LangGraph** – agentic control flow  
- **Ollama** – local LLM inference  
- **Custom Tools** – repo parsing, commit summarization, code quality checks  

---

## 🧩 Project Structure
```
├── agent.py              # Main conversational agent (LangGraph + Ollama)
├── load_repo.py          # Clones or loads the GitHub repo locally
├── tools_loader.py       # Loads all custom analysis tools
├── CONFIG.py             # Contains model and repo path configuration
├── requirements.txt      # All required dependencies
└── README.md             # You are here
```

---

## 🧰 Setup Instructions

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Load your repository
Clone or import your target GitHub repo locally:
```bash
python load_repo.py
```

### 3️⃣ Run the AI agent
Start the interactive code analysis agent:
```bash
python agent.py
```

You’ll see:
```
GitHub Project Analyzer (type 'exit' or 'quit' to stop)
You:
```
Ask questions like:
- “What’s the main purpose of this repo?”
- “Summarize the latest commits.”
- “Which files lack docstrings?”
- “How is the complexity of the core module?”

---

## 🧠 Example Conversation
```
You: Analyze the repo structure
Agent: The repository contains modules for core logic, data utils, and API integration...
```

---

## 🪄 Future Improvements
- Add vector-based semantic code retrieval  
- Integrate code-style linting reports  
- Support for multiple repos and diff comparison  

---

## 💬 Author
**Built by:** *Prashant Raj*  
Inspired by the idea of bringing **local AI code intelligence** closer to every developer.  
