require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();
const port = process.env.PORT || 3000;

// Middleware для парсинга тела запроса
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Главная страница
app.get('/', (req, res) => {
    res.send('<h1>Task Tracker Web App</h1><form action="/add-task" method="post"><input type="text" name="task" placeholder="Enter task"><button type="submit">Add Task</button></form>');
});

// Обработка добавления задачи
app.post('/add-task', async (req, res) => {
    const task = req.body.task;
    try {
        const response = await axios.post(`https://api.telegram.org/bot${process.env.BOT_TOKEN}/sendMessage`, {
            chat_id: process.env.CHAT_ID,
            text: `New task added: ${task}`
        });
        res.send('Task added successfully');
    } catch (error) {
        console.error(error);
        res.send('Failed to add task');
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
