# 🖥️ Python-Based Command Terminal (Hackathon Project)

## 📌 Overview
This project is built for the **CodeMate Hackathon** under the problem statement:

> **Develop a fully functioning command terminal that mimics the behavior of a real system terminal.**  
> The backend of this terminal is powered by Python (Flask), and it can process and execute standard commands.  
> It also provides a simple **web-based UI** for interaction.

---

## ✨ Features
- ✅ **Python Backend** – Executes commands securely using `subprocess`  
- ✅ **File & Directory Operations** – Supports commands like `ls`, `pwd`, `mkdir`, `rm`, etc.  
- ✅ **Error Handling** – Invalid commands return clean error messages  
- ✅ **Web Interface** – Access via `/static/index.html`  
- ✅ **Deployed Online** – Runs on Render (cloud hosting)  
- ⚡ **Optional**: Extend with AI-driven natural language commands  

---

## 🛠️ Tech Stack
- **Backend**: Python, Flask  
- **Frontend**: HTML, CSS, JavaScript (minimal static page)  
- **Deployment**: Render (Gunicorn + Flask)  
- **Version Control**: Git + GitHub  

---

## 🚀 Live Demo
🔗 [Try the Terminal in Browser](https://python-terminal-hack.onrender.com/static/index.html)  

Example API Test:
```bash
curl -sS -X POST https://python-terminal-hack.onrender.com/local_run \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"print(\"hello from deployed runner\")"}'
