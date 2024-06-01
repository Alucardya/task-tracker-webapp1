import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel, Container } from '@mui/material';

function TaskForm({ onTaskAdded }) {
  const [task, setTask] = useState('');
  const [category, setCategory] = useState('');
  const [priority, setPriority] = useState('Средний');
  const [notes, setNotes] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newTask = { user_id: 1, task, category, priority, notes }; // Replace user_id with dynamic value if needed
    await axios.post('/api/tasks', newTask);
    onTaskAdded();
  };

  return (
    <Container>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Task"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          required
          fullWidth
          margin="normal"
        />
        <TextField
          label="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          fullWidth
          margin="normal"
        />
        <FormControl fullWidth margin="normal">
          <InputLabel>Priority</InputLabel>
          <Select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <MenuItem value="Высокий">Высокий</MenuItem>
            <MenuItem value="Средний">Средний</MenuItem>
            <MenuItem value="Низкий">Низкий</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="Notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          fullWidth
          multiline
          rows={4}
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary">Add Task</Button>
      </form>
    </Container>
  );
}

export default TaskForm;
