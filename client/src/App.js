import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, AppBar, Typography, TextField, Button, List, ListItem, ListItemText, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const App = () => {
  const [tasks, setTasks] = useState([]);
  const [task, setTask] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const response = await axios.get('/api/tasks');
    setTasks(response.data);
  };

  const addTask = async () => {
    if (task) {
      await axios.post('/api/tasks', { task });
      setTask('');
      fetchTasks();
    }
  };

  const deleteTask = async (id) => {
    await axios.delete(`/api/tasks/${id}`);
    fetchTasks();
  };

  return (
    <Container>
      <AppBar position="static" style={{ marginBottom: '20px' }}>
        <Typography variant="h6" style={{ padding: '10px' }}>
          Task Tracker
        </Typography>
      </AppBar>
      <TextField
        label="New Task"
        variant="outlined"
        fullWidth
        value={task}
        onChange={(e) => setTask(e.target.value)}
        style={{ marginBottom: '20px' }}
      />
      <Button variant="contained" color="primary" onClick={addTask}>
        Add Task
      </Button>
      <List>
        {tasks.map((task) => (
          <ListItem key={task.id} style={{ marginTop: '10px' }}>
            <ListItemText primary={task.task} />
            <IconButton edge="end" aria-label="delete" onClick={() => deleteTask(task.id)}>
              <DeleteIcon />
            </IconButton>
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default App;
