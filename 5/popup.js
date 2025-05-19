document.getElementById("select").addEventListener("click", () => {
    chrome.tabs.executeScript({ file: "content.js" });
  });
  
  document.getElementById("send").addEventListener("click", async () => {
    chrome.storage.local.get(["selectedElement"], async (data) => {
      let selector = data.selectedElement;
      let url = await getCurrentTabUrl();
  
      fetch("http://localhost:8000/data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url, cssSelector: selector })
      }).then(response => response.json())
        .then(data => document.getElementById("status").innerText = "ID: " + data)
        .catch(error => console.error("Ошибка:", error));
    });
  });
  
  async function getCurrentTabUrl() {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab.url;
  }
  