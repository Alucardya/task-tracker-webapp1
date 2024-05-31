require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const { exec } = require('child_process');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware for parsing request body
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Initialize the database
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

// Start the bot
const startBot = () => {
    console.log('Starting bot...');
    exec('python bot.py', (err, stdout, stderr) => {
        if (err) {
            console.error(`Error starting bot: ${err}`);
            return;
        }
        console.log(`Bot started: ${stdout}`);
        if (stderr) {
            console.error(`Bot error: ${stderr}`);
        }
    });
};

// Handle task addition
app.post('/add-task', (req, res) => {
    const { task, category, priority, notes } = req.body;
    const user_id = process.env.CHAT_ID;

    const db = new sqlite3.Database('task_tracker.db');
    db.run('INSERT INTO tasks (user_id, task, category, priority, notes) VALUES (?, ?, ?, ?, ?)',
        [user_id, task, category || 'No Category', priority || 'Medium', notes || ''], (err) => {
            if (err) {
                return console.log(err.message);
            }
            axios.post(`https://api.telegram.org/bot${process.env.BOT_TOKEN}/sendMessage`, {
                chat_id: user_id,
                text: `New task added: ${task}`
            });
            res.send('Task added successfully');
        });
    db.close();
});

// Handle task display
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

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '../task-tracker-react/build')));

// The "catchall" handler: for any request that doesn't match one above, send back index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../task-tracker-react/build', 'index.html'));
});

app.listen(PORT, () => {
    initDb();
    startBot();
    console.log(`Server is running on port ${PORT}`);
});
