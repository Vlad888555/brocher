document.getElementById('getURL').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    document.getElementById('output').textContent = `Current URL: ${tab.url}`;
  });
  
  document.getElementById('selectElement').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js'],
    });
    
  });
  
document.getElementById('log').addEventListener("click", ()=>{
  // const url = chrome.runtime.getURL("reg.html");
  chrome.tabs.create({ url : "http://localhost/test1/index.php" });
  window.close();
})

document.getElementById('reg').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['q.js'],
  });
});