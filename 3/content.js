let highlightStyle = `
  outline: 2px solid red;
  background-color: rgba(255, 0, 0, 0.2);
`;

function enableSelection() {
  document.body.style.cursor = 'crosshair';

  let lastHighlightedElement = null; // Для снятия подсветки с предыдущего элемента

  const mouseOverHandler = (event) => {
    if (lastHighlightedElement) {
      lastHighlightedElement.style.cssText = lastHighlightedElement.style.cssText.replace(highlightStyle, '');
    }
    lastHighlightedElement = event.target; // Обновляем последний подсвеченный элемент
    event.target.style.cssText += highlightStyle;
  };

  const clickHandler = (event) => {
    event.preventDefault();
    event.stopPropagation();
    document.body.style.cursor = '';

    // Убираем подсветку с выбранного элемента
    if (lastHighlightedElement) {
      lastHighlightedElement.style.cssText = lastHighlightedElement.style.cssText.replace(highlightStyle, '');
    }

    // Очищаем обработчики событий
    document.removeEventListener('mouseover', mouseOverHandler);
    document.removeEventListener('click', clickHandler);
    const currentUrl = window.location.href;

    // Получаем только данные родительского элемента
    const selectedElementInfo = {
      url: currentUrl,
      tag: event.target.tagName, // Тег элемента
      id: event.target.id || null, // ID элемента, если есть
      classList: [...event.target.classList], // Список классов элемента
      textContent: event.target.textContent.trim() // Текст элемента
    };

    console.log('Selected Element Info:', selectedElementInfo);
    alert(`Selected Element Info:\n${JSON.stringify(selectedElementInfo, null, 2)}`);
  };

  document.addEventListener('mouseover', mouseOverHandler);
  document.addEventListener('click', clickHandler);
}

enableSelection();
