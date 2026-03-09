document.getElementById('btn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const msg = document.getElementById('msg');
  msg.innerText = "Scanning...";

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const sidebar = document.querySelector('[class*="transcript-panel"]') || 
                      document.querySelector('[class*="transcript--transcript-container"]') ||
                      document.querySelector('div[data-purpose="transcript-panel"]');
      
      if (!sidebar) return "ERROR: Sidebar not found. Is it open?";

      const text = sidebar.innerText;
      const cleanedText = text.replace(/^\d+:\d+\s*$/gm, '').replace(/\n+/g, ' ').trim();

      return cleanedText.length > 20 ? cleanedText : "ERROR: Sidebar found but it seems empty.";
    }
  }, (results) => {
    const resultText = results[0].result; // This is the transcript text
    
    if (resultText.startsWith("ERROR")) {
      msg.innerText = resultText;
      return;
    }

    msg.innerText = "Sending " + resultText.length + " chars...";

    // --- NEW SECURITY BLOCK START ---
    chrome.storage.local.get(['bridgeKey'], (storage) => {
      if (!storage.bridgeKey) {
        msg.innerText = "❌ No API Key! Check Options.";
        return;
      }

      fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "X-Ollama-Bridge-Key": storage.bridgeKey 
        },
        body: JSON.stringify({ text: resultText })
      })
      .then(response => {
        if (response.status === 401) throw new Error("Invalid Key");
        msg.innerText = "✅ Success!";
      })
      .catch((err) => { 
        msg.innerText = err.message === "Invalid Key" ? "❌ Wrong API Key" : "❌ Server error"; 
      });
    });
    // --- NEW SECURITY BLOCK END ---
  });
});