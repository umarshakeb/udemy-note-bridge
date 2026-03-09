import requests
import json
import datetime
import os        # Added: Required for os.path.exists
import secrets   # Added: Required for generating the hex token
from flask import Flask, request, jsonify, abort # Added: abort
from flask_cors import CORS
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

notes_dir = ROOT_DIR / "notes"
notes_dir.mkdir(exist_ok=True)

app = Flask(__name__)

# SECURITY: Generate a secret key if it doesn't exist
CONFIG_FILE = "auth_config.json"
if not os.path.exists(CONFIG_FILE):
    auth_key = secrets.token_hex(16)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": auth_key}, f)
else:
    with open(CONFIG_FILE, "r") as f:
        auth_key = json.load(f).get("api_key")

CORS(app) # For local use, this is fine. For Pro, we'd restrict it.

@app.before_request
def verify_token():
    # Only allow requests that carry our secret token in the header
    user_token = request.headers.get("X-Ollama-Bridge-Key")
    if user_token != auth_key:
        print(f"⚠️ Unauthorized access attempt from {request.remote_addr}")
        abort(401) 

OLLAMA_API = "http://localhost:11434/api/generate"

@app.route('/summarize', methods=['POST'])
def handle_summary():
    try:
        data = request.json
        text_content = data.get("text", "")

        if not text_content:
            return jsonify({"status": "error", "message": "No text received"}), 400

        print(f"--- Received {len(text_content)} characters. Contacting Ollama... ---")

        prompt = (
            "Use this transcript to prepare in depth notes as structured bullet point. "
            "Focus on what concepts were taught and what definitions were provided.\n\n"
            f"TRANSCRIPT:\n{text_content}"
        )

        # 1. Send to Ollama
        response = requests.post(OLLAMA_API, json={
            "model": "llama3.2", 
            "prompt": prompt,
            "stream": False
        }, timeout=None) 

        if response.status_code != 200:
            print(f"Ollama Error: {response.text}")
            return jsonify({"status": "error", "message": "Ollama failed"}), 500

        summary = response.json().get("response", "")

        # 2. Save the file (Fixed datetime calls)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M")
        filename = f"udemy_notes_{timestamp}.md"
        file_path = os.path.join(notes_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"\n\n# Lesson @ {now.strftime('%H:%M:%S')}\n")
            f.write(summary)
            f.write("\n\n---\n")

        print(f"✅ SUCCESS: Notes saved to {filename}")
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"❌ CRASH LOG: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print(f"--- SERVER SECURED ---")
    print(f"Your API Key is: {auth_key}")
    print(f"Add this key to your extension settings.")
    print("Python Bridge is running on http://localhost:5000")
    app.run(host='127.0.0.1', port=5000)