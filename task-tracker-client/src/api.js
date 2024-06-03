import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [tasks, setTasks] = useState([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    useEffect(() => {
        axios.get('/tasks')
            .then(response => setTasks(response.data))
            .catch(error => console.log(error));
    }, []);

    const addTask = () => {
        axios.post('/tasks', { title, description })
            .then(response => {
                setTasks([...tasks, { title, description, completed: false }]);
                setTitle('');
                setDescription('');
            })
            .catch(error => console.log(error));
    };

    return (
        <div>
            <h1>Task Tracker</h1>
            <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <input
                type="text"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <button onClick={addTask}>Add Task</button>
            <ul>
                {tasks.map((task, index) => (
                    <li key={index}>{task.title}: {task.description}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
