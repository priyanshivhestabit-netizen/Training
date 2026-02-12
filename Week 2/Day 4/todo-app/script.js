document.addEventListener("DOMContentLoaded",init);

function init(){
    try{
        renderTodos(loadFromStorage());
        setupEventListeners();
    }catch(error){
        console.error("Initialization Error:",error);
    }
}

function setupEventListeners(){
    const form=document.getElementById("todo-form");

    form.addEventListener("submit",function(e){
        e.preventDefault();

        const input = document.getElementById("todo-input");
        const text=input.value.trim();

        if(!text) return;

        addTodo(text);
        input.value=""
    });
}

//CRUD operations
function addTodo(text){
    try{
        const todos = loadFromStorage();

        const newTodo = {
            id: Date.now().toString(),
            text,
            completed:false,
        };

        todos.push(newTodo);
        saveToStorage(todos);
        renderTodos(todos);
    }
    catch(error){
        console.error("error adding task");
    }
}

function deleteTodo(id){
    try{
        const todos=loadFromStorage();
        const updated=todos.filter(todo => todo.id !== id);

        saveToStorage(updated);
        renderTodos(updated);
    }
    catch(error){
    console.error("deletion error");
    }
}

function toggleComplete(id) {
  try {
    const todos = loadFromStorage();

    const updated = todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );

    saveToStorage(updated);
    renderTodos(updated);
  } catch (error) {
    console.error("Toggle Error:", error);
  }
}

function editTodo(id) {
  try {
    const todos = loadFromStorage();
    const todo = todos.find(t => t.id === id);

    const newText = prompt("Edit your task:", todo.text);

    if (newText === null) return;

    const updated = todos.map(t =>
      t.id === id ? { ...t, text: newText.trim() || t.text } : t
    );

    saveToStorage(updated);
    renderTodos(updated);
  } catch (error) {
    console.error("Edit Error:", error);
  }
}


function renderTodos(todos) {
  const list = document.getElementById("todo-list");
  list.innerHTML = "";

  todos.forEach(todo => {
    const li = document.createElement("li");

    if (todo.completed) {
      li.classList.add("completed");
    }

    li.innerHTML = `
      <span onclick="toggleComplete('${todo.id}')">${todo.text}</span>
      <div class="actions">
        <button onclick="editTodo('${todo.id}')">Edit</button>
        <button class="delete" onclick="deleteTodo('${todo.id}')">Delete</button>
      </div>
    `;

    list.appendChild(li);
  });
}


function saveToStorage(data) {
  localStorage.setItem("todos", JSON.stringify(data));
}

function loadFromStorage() {
  return JSON.parse(localStorage.getItem("todos")) || [];
}
