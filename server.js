require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const { exec } = require('child_process');
const path = require('path');
const app = express();
const port = process.env.PORT || 8443;

// Middleware для парсинга тела запроса
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Ініціалізація бази даних
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

// Обробка додавання задачі
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

// Обробка відображення задач
app.get('/show-tasks', (req, res) => {
    const user_id = process.env.CHAT_ID;

    const db = new sqlite3.Database('task_tracker.db');
    db.all('SELECT task, category, priority, notes FROM tasks WHERE user_id = ?', [user_id], (err, rows) => {
        if (err) {
            return console.log(err.message);
        }
        res.json(rows);
    });
    db.close();
});

// Вказуємо серверу обслуговувати статичні файли з папки build
app.use(express.static(path.join(__dirname, 'task-tracker-react/build')));

// Відправляємо всі запити на головну сторінку React додатка
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'task-tracker-react/build', 'index.html'));
});

app.listen(port, () => {
    initDb();
    startBot();
    console.log(`Сервер працює на порту ${port}`);
});
