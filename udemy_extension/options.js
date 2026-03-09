// Load the key when the page opens
document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get(['bridgeKey'], (result) => {
    if (result.bridgeKey) {
      document.getElementById('apiKey').value = result.bridgeKey;
    }
  });
});

// Save the key
document.getElementById('save').addEventListener('click', () => {
  const key = document.getElementById('apiKey').value;
  chrome.storage.local.set({ bridgeKey: key }, () => {
    alert('Key saved securely!');
  });
});