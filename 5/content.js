let isInspecting = false;

function getElementInfo(element) {
  const selector = getUniqueSelector(element);
  const similarElements = document.querySelectorAll(selector);
  
  return {
    tag: element.tagName,
    id: element.id,
    classes: Array.from(element.classList),
    attributes: Array.from(element.attributes).map(attr => ({
      name: attr.name,
      value: attr.value
    })),
    unique: similarElements.length === 1,
    count: similarElements.length,
    selector: selector
  };
}

function getUniqueSelector(element) {
  const path = [];
  while (element && element.nodeType === Node.ELEMENT_NODE) {
    let selector = element.nodeName.toLowerCase();
    
    if (element.id) {
      selector += `#${element.id}`;
      path.unshift(selector);
      break;
    } else {
      let sibling = element;
      let nth = 1;
      while (sibling !== element.parentNode.firstChild) {
        sibling = sibling.previousElementSibling;
        nth++;
      }
      selector += `:nth-child(${nth})`;
    }
    path.unshift(selector);
    element = element.parentNode;
  }
  return path.join(' > ');
}

function highlightElement(element) {
  element.style.outline = '2px solid red';
  setTimeout(() => element.style.outline = '', 500);
}

function handleClick(event) {
  event.preventDefault();
  event.stopPropagation();
  
  const element = event.target;
  const info = getElementInfo(element);
  
  highlightElement(element);
  
  const result = `Tag: ${info.tag}
Unique: ${info.unique ? 'Yes' : 'No'}
Count: ${info.count}
Selector: ${info.selector}
ID: ${info.id || 'None'}
Classes: ${info.classes.join(', ') || 'None'}`;

  alert(result);
}

function startInspection() {
  if (!isInspecting) {
    document.addEventListener('click', handleClick, true);
    isInspecting = true;
  } else {
    document.removeEventListener('click', handleClick, true);
    isInspecting = false;
  }
}

// Start inspection when injected
startInspection();