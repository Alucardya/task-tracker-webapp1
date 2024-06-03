import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchTasks, addTask as addTaskApi } from './api';

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

  const addTask = async (task) => {
    try {
      const newTask = await addTaskApi(task);
      setTasks([...tasks, newTask]);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <TaskContext.Provider value={{ tasks, setTasks, addTask }}>
      {children}
    </TaskContext.Provider>
  );
};

const useTasks = () => {
  return useContext(TaskContext);
};

export { TaskProvider, TaskContext, useTasks };
