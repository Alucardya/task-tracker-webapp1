require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const { exec } = require('child_process');
const app = express();
const port = process.env.PORT || 3000;

// Middleware для парсинга тела запроса
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Инициализация базы данных
const initDb = () => {
    const db = new sqlite3.Database('task_tracker.db');
    db.run(`
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            task TEXT,
            category TEXT,
            priority TEXT,
            notes TEXT
        )
    `);
    db.close();
};

// Запуск бота
const startBot = () => {
    console.log('Запуск бота...');
    exec('python bot.py', (err, stdout, stderr) => {
        if (err) {
            console.error(`Ошибка при запуске бота: ${err}`);
            return;
        }
        console.log(`Бот запущен: ${stdout}`);
        if (stderr) {
            console.error(`Ошибка бота: ${stderr}`);
        }
    });
};

// Главная страница
app.get('/', (req, res) => {
    res.send(`
        <h1>Task Tracker Web App</h1>
        <form action="/add-task" method="post">
            <input type="text" name="task" placeholder="Введіть задачу" required>
            <input type="text" name="category" placeholder="Введіть категорію">
            <input type="text" name="priority" placeholder="Введіть пріоритет">
            <textarea name="notes" placeholder="Введіть нотатки"></textarea>
            <button type="submit">Додати задачу</button>
        </form>
        <form action="/show-tasks" method="get">
            <button type="submit">Показати задачі</button>
        </form>
    `);
});

// Обработка добавления задачи
app.post('/add-task', (req, res) => {
    const { task, category, priority, notes } = req.body;
    const user_id = process.env.CHAT_ID;

    const db = new sqlite3.Database('task_tracker.db');
    db.run('INSERT INTO tasks (user_id, task, category, priority, notes) VALUES (?, ?, ?, ?, ?)',
        [user_id, task, category || 'Без категорії', priority || 'Середній', notes || ''], (err) => {
            if (err) {
                return console.log(err.message);
            }
            axios.post(`https://api.telegram.org/bot${process.env.BOT_TOKEN}/sendMessage`, {
                chat_id: user_id,
                text: `Нова задача додана: ${task}`
            });
            res.send('Задача додана успішно');
        });
    db.close();
});

// Обработка отображения задач
app.get('/show-tasks', (req, res) => {
    const user_id = process.env.CHAT_ID;

    const db = new sqlite3.Database('task_tracker.db');
    db.all('SELECT task, category, priority, notes FROM tasks WHERE user_id = ?', [user_id], (err, rows) => {
        if (err) {
            return console.log(err.message);
        }
        let tasks = 'Ваші задачі:\n';
        rows.forEach((row) => {
            tasks += `${row.task} [${row.category}] - пріоритет: ${row.priority}, нотатки: ${row.notes}\n`;
        });
        res.send(tasks);
    });
    db.close();
});

app.listen(port, () => {
    initDb();
    startBot();
    console.log(`Сервер працює на порту ${port}`);
});
