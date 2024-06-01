from flask import Flask, send_from_directory, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  # Удалил WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import sqlite3
import logging

# Создание экземпляра Flask
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функции для работы с базой данных SQLite
def init_db():
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      description TEXT)''')
    conn.commit()
    conn.close()

def add_task(title, description):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# Telegram бот функции
async def start(update: Update, context):
    await update.message.reply_text("Welcome to Task Tracker Bot!")

async def add_task_command(update: Update, context):
    args = context.args
    if len(args) == 0:
        await update.message.reply_text("Please provide the task title.")
    else:
        title = ' '.join(args)
        add_task(title, "")
        await update.message.reply_text(f'Task "{title}" added!')

async def list_tasks_command(update: Update, context):
    tasks = get_tasks()
    if len(tasks) == 0:
        await update.message.reply_text("No tasks found.")
    else:
        message = "\n".join([f'{task[0]}: {task[1]}' for task in tasks])
        await update.message.reply_text(message)

async def delete_task_command(update: Update, context):
    args = context.args
    if len(args) == 0:
        await update.message.reply_text("Please provide the task ID to delete.")
    else:
        task_id = int(args[0])
        delete_task(task_id)
        await update.message.reply_text(f'Task {task_id} deleted!')

# Запуск Telegram бота
def run_bot():
    application = ApplicationBuilder().token(os.environ['TELEGRAM_TOKEN']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task_command))
    application.add_handler(CommandHandler("list", list_tasks_command))
    application.add_handler(CommandHandler("delete", delete_task_command))

    application.run_polling()

# Flask маршруты
@app.route('/')
def index():
    return "Welcome to Task Tracker!"

@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = get_tasks()
    return json.dumps(tasks)

@app.route('/add_task', methods=['POST'])
def add_task_route():
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    add_task(title, description)
    return 'Task added successfully!'

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return 'Task deleted successfully!'

# Инициализация базы данных
init_db()

# Запуск бота в фоновом режиме
scheduler = BackgroundScheduler()
scheduler.add_job(run_bot, 'interval', seconds=10)
scheduler.start()

# Запуск Flask приложения
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
