import React, { useEffect } from 'react';
import { Container } from '@mui/material';
import { fetchTasks, addTask as addTaskApi, updateTask, deleteTask as deleteTaskApi } from './api';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import { useTasks } from './TaskContext';

function App() {
  const { tasks, setTasks, addTask, updateTaskContext, deleteTask } = useTasks();

  useEffect(() => {
    const getTasks = async () => {
      try {
        const tasks = await fetchTasks();
        setTasks(Array.isArray(tasks) ? tasks : []);
      } catch (error) {
        console.error(error);
        setTasks([]);
      }
    };

    getTasks();
  }, [setTasks]);

  const handleAddTask = async (task) => {
    try {
      const newTask = await addTaskApi(task);
      addTask({ ...newTask, completed: false });
    } catch (error) {
      console.error(error);
    }
  };

  const handleComplete = async (taskId) => {
    try {
      const updatedTask = await updateTask(taskId, {
        completed: !tasks.find((task) => task.id === taskId).completed,
      });
      updateTaskContext(updatedTask);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (taskId) => {
    try {
      await deleteTaskApi(taskId);
      deleteTask(taskId);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container>
      <h1>Task Tracker</h1>
      <TaskForm onTaskAdded={handleAddTask} />
      <TaskList tasks={tasks} onComplete={handleComplete} onDelete={handleDelete} />
    </Container>
  );
}

export default App;
