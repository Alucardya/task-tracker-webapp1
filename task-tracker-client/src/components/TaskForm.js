import React, { useState, useContext } from 'react';
import { TaskContext } from '../TaskContext';
import { TextField, Button, Container } from '@mui/material';

function TaskForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const { addTask } = useContext(TaskContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newTask = { title, description };
      addTask(newTask); // Use addTask context function
      setTitle('');
      setDescription('');
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Container>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          fullWidth
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary">Add Task</Button>
      </form>
    </Container>
  );
}

export default TaskForm;
