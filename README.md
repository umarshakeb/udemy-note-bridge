# 🎓 Udemy Transcript Note Bridge

An **AI-powered Chrome Extension** that bridges the gap between your **Udemy learning** and **local intelligence**.

It extracts course transcripts and sends them to a **local Ollama server** to generate **structured, in-depth study notes** automatically.

---

# 🚀 Features

### 🔒 Privacy First
Everything runs **locally on your machine**.  
No transcripts or learning data are sent to external cloud servers.

### 🤖 AI-Powered Summarization
Uses **locally hosted LLMs** (such as `llama3.2`) through **Ollama** to analyze course transcripts.

### 🧠 Structured Study Notes
Automatically generates **clean Markdown notes** including:

- Key concepts
- Definitions
- Bullet point explanations
- Structured summaries

### 🔑 Secure Local Bridge
Communication between the browser extension and your local server is **authenticated using secret API keys**.

---

# 🛠 Prerequisites

Before installing, make sure you have the following:

- **Python 3.10+**
- **Ollama installed**
- An Ollama model such as: llama3.2


Install a model if needed:

```bash
ollama pull llama3.2
```

### Google Chrome Browser
- ⚙️ Setup Instructions
- 1️⃣ Start the Python Bridge

This local server acts as the gateway between the extension and your AI model.

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/udemy-note-bridge.git
cd udemy-note-bridge
```
### Install Dependencies
```bash
pip install flask flask-cors requests
```
### Run the Server
```bash
python study_server.py
```
On the first launch, the server will generate:
```bash
auth_config.json
```
The terminal will display a generated API key.

📌 Copy this API key — you will need it in the Chrome extension.

## 2️⃣ Install the Chrome Extension

* Open Chrome and navigate to:
```bash
chrome://extensions/
```
* Enable **Developer Mode (top-right toggle)**.
* Click **Load** unpacked.
* Select the folder:
```bash
udemy_extension
```
* Click the extension icon → open Options.  
* Paste the API key generated earlier.  
* Click Save.  
Your extension is now connected to your local AI server.

### 🧩 How It Works

1️⃣ The extension extracts Udemy transcript text.  
2️⃣ The transcript is sent to the local Flask bridge server.  
3️⃣ The bridge server sends it to Ollama.  
4️⃣ The LLM generates structured study notes.  
5️⃣ The notes are returned as Markdown.  

Everything happens **locally** on your machine.

### 🛡 Security & Privacy

* This project follows a **Zero Trust local architecture.**  
* All transcript processing occurs **locally**  
* The server listens only on:
```bash
127.0.0.1 (localhost)
```
* API authentication header:
```bash
X-Ollama-Bridge-Key
```
This ensures that only your **browser extension can communicate with the server.**

### 📂 Project Structure
```bash
udemy-note-bridge/
│
├── study_server.py
├── auth_config.json
├── requirements.txt
│
├── udemy_extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   └── options.html
│
└── README.md
```

### 🧠 Customization

You can customize the prompt logic inside:
```bash
study_server.py
```
Examples:
1. Generate flashcards  
2. Generate exam-style questions  
3. Generate detailed concept explanations  
4. Convert notes into Notion format

### 📝 License
This project is **open-source**.  
Feel free to:
* Fork the repository  
* Customize prompts  
* Extend the extension functionality  
* Add support for other learning platforms  

⭐ If you find this useful, consider starring the repo!
