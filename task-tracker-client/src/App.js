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
            <div>
                <label htmlFor="task-title">Title</label>
                <input
                    type="text"
                    id="task-title"
                    name="title"
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="task-description">Description</label>
                <input
                    type="text"
                    id="task-description"
                    name="description"
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
            </div>
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
