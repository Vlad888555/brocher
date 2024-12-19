let highlightStyle = `
  outline: 2px solid red;
  background-color: rgba(255, 0, 0, 0.2);
`;

function enableSelection() {
  document.body.style.cursor = 'crosshair';

  let lastHighlightedElement = null;
  let otvet = null;

  //путь к элементу
  const getCssSelector = (element) => {
    const parts = [];
    while (element.parentElement) {
      const tagName = element.tagName.toLowerCase();
      const id = element.id ? `#${element.id}` : '';
      const classes = [...element.classList].map(cls => `.${cls}`).join('');
      const siblingIndex = Array.from(element.parentElement.children).indexOf(element) + 1;

      parts.unshift(`${tagName}${id}${classes}:nth-child(${siblingIndex})`);
      element = element.parentElement;
    }
    return parts.join(' > ');
  };


  const mouseOverHandler = (event) => {
    if (lastHighlightedElement) {
      lastHighlightedElement.style.cssText = lastHighlightedElement.style.cssText.replace(highlightStyle, '');
    }
    lastHighlightedElement = event.target;
    event.target.style.cssText += highlightStyle;
  };

  const clickHandler = (event) => {
    event.preventDefault();
    event.stopPropagation();
    document.body.style.cursor = '';

    if (lastHighlightedElement) {
      lastHighlightedElement.style.cssText = lastHighlightedElement.style.cssText.replace(highlightStyle, '');
    }
    if (localStorage.getItem("example.txt")){
      storage = 1;
    }else{
      storage = 0;
    }

    document.removeEventListener('mouseover', mouseOverHandler);
    document.removeEventListener('click', clickHandler);
    const currentUrl = window.location.href;
    const selectedElementInfo = {
      cssSelector: getCssSelector(event.target),
      url: currentUrl,
      textContent: event.target.textContent.trim(),
      localStorage: storage,
    };

    //на сервер
    const apiUrl = "http://127.0.0.1:8000/data";

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(selectedElementInfo),
    })
      .then(response => {
        console.log('Raw Response:', response);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Parsed JSON:', data);
        otvet = JSON.stringify(data)
        alert(otvet)
        if (otvet != 0){
          localStorage.setItem("example.txt", otvet);
          console.log(`File "example.txt" saved to localStorage.`);
        }
      })
      .catch(error => {
        console.error('Fetch Error:', error.message);
      });
  };
  document.addEventListener('mouseover', mouseOverHandler);
  document.addEventListener('click', clickHandler);
}

enableSelection();