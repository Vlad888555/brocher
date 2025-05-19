chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getElementInfo") {
      // Handle messages if needed
    }
  });