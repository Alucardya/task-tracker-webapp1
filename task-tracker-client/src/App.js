import React, { useState, useEffect } from 'react';
import { fetchTasks, addTask as addTaskApi } from './api';

function App() {
    const [tasks, setTasks] = useState([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

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

    const addTask = async () => {
        try {
            const newTask = await addTaskApi({ title, description });
            setTasks([...tasks, { ...newTask, completed: false }]);
            setTitle('');
            setDescription('');
        } catch (error) {
            console.log(error);
        }
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
