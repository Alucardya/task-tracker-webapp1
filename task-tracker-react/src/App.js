// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function TaskForm({ addTask }) {
  const [task, setTask] = useState('');
  const [category, setCategory] = useState('');
  const [priority, setPriority] = useState('');
  const [notes, setNotes] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/add-task', { task, category, priority, notes });
      addTask({ task, category, priority, notes });
      setTask('');
      setCategory('');
      setPriority('');
      setNotes('');
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={task} onChange={(e) => setTask(e.target.value)} placeholder="Введіть задачу" required />
      <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Введіть категорію" />
      <input type="text" value={priority} onChange={(e) => setPriority(e.target.value)} placeholder="Введіть пріоритет" />
      <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Введіть нотатки"></textarea>
      <button type="submit">Додати задачу</button>
    </form>
  );
}

function TaskList() {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    try {
      const response = await axios.get('/show-tasks');
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  return (
    <div>
      <h2>Task List</h2>
      <button onClick={fetchTasks}>Завантажити задачі</button>
      <ul>
        {tasks.map((task, index) => (
          <li key={index} className="task-item">
            <h3>{task.task}</h3>
            <p>Категорія: {task.category}</p>
            <p>Пріоритет: {task.priority}</p>
            <p>Нотатки: {task.notes}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

function App() {
  const [tasks, setTasks] = useState([]);

  const addTask = (newTask) => {
    setTasks([...tasks, newTask]);
  };

  return (
    <div className="App">
      <h1>Task Tracker Web App</h1>
      <TaskForm addTask={addTask} />
      <TaskList />
    </div>
  );
}

export default App;
