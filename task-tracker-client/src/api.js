import axios from 'axios';

export const fetchTasks = async () => {
    try {
        const response = await axios.get('http://localhost:5000/tasks/');
        return response.data;
    } catch (error) {
        console.error('Error fetching tasks:', error);
        throw error;
    }
};

export const addTask = async (task) => {
    try {
        const response = await axios.post('http://localhost:5000/tasks/', task);
        return response.data;
    } catch (error) {
        console.error('Error adding task:', error);
        throw error;
    }
};
