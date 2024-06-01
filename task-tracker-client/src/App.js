// src/App.js
import React, { useState, useEffect } from 'react';
import TaskList from './components/TaskList';
import AddTask from './components/AddTask';
import { fetchTasks, addTask } from './api';
import './App.css';

const App = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const getTasks = async () => {
      const tasksFromServer = await fetchTasks();
      setTasks(tasksFromServer);
    };

    getTasks();
  }, []);

  const addNewTask = async (title) => {
    const newTask = await addTask({ title });
    setTasks([...tasks, newTask]);
  };

  return (
    <div className="App">
      <h1>Task Tracker</h1>
      <AddTask onAdd={addNewTask} />
      <TaskList tasks={tasks} />
    </div>
  );
};

export default App;
