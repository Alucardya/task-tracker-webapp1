import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchTasks } from './api';

const TaskContext = createContext();

const TaskProvider = ({ children }) => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const getTasks = async () => {
      try {
        const tasks = await fetchTasks();
        setTasks(Array.isArray(tasks) ? tasks : []);
      } catch (error) {
        console.log(error);
        setTasks([]);
      }
    };

    getTasks();
  }, []);

  const addTask = (task) => {
    setTasks([...tasks, task]);
  };

  const updateTaskContext = (updatedTask) => {
    setTasks(tasks.map(task => (task.id === updatedTask.id ? updatedTask : task)));
  };

  const deleteTask = (taskId) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  return (
    <TaskContext.Provider value={{ tasks, setTasks, addTask, updateTaskContext, deleteTask }}>
      {children}
    </TaskContext.Provider>
  );
};

const useTasks = () => {
  return useContext(TaskContext);
};

export { TaskProvider, TaskContext, useTasks };
