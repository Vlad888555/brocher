let highlightStyle = `
  outline: 2px solid red;
  background-color: rgba(255, 0, 0, 0.2);
`;

function enableSelection() {
  document.body.style.cursor = 'crosshair';

  let lastHighlightedElement = null;

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

    document.removeEventListener('mouseover', mouseOverHandler);
    document.removeEventListener('click', clickHandler);
    const currentUrl = window.location.href;
    const selectedElementInfo = {
      cssSelector: getCssSelector(event.target),
      url: currentUrl,
      textContent: event.target.textContent.trim(),
    };

    console.log('Selected Element Info:', selectedElementInfo);
    // alert(`Selected Element Info:\n${JSON.stringify(selectedElementInfo, null, 2)}`);

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
        console.log('Raw Response:', response); // Логируем ответ целиком
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Пробуем обработать JSON
      })
      .then(data => {
        console.log('Parsed JSON:', data);
        alert(JSON.stringify(data))
      })
      .catch(error => {
        console.error('Fetch Error:', error.message);
      });
  };

  document.addEventListener('mouseover', mouseOverHandler);
  document.addEventListener('click', clickHandler);
}

enableSelection();