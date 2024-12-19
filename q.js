 // Функция чтения файла из localStorage
 function readFileLocalStorage(fileName) {
    const content = localStorage.getItem(fileName);
    if (content) {
      console.log(`File content: ${content}`);
      alert(`File content: ${content}`);
    } else {
      console.log(`File "${fileName}" not found.`);
    }
  }
  readFileLocalStorage("example.txt");