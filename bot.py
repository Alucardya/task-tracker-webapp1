import os
import sqlite3
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка Flask
app = Flask(__name__)

# Настройка токена
TOKEN = '6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg'
bot = Bot(token=TOKEN)

# Функции для работы с базой данных SQLite
def init_db():
    conn = sqlite3.connect('task_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect('task_tracker.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('task_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect('task_tracker.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Обработчики команд
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the conversation.")
    update.message.reply_text(
        'Welcome! You can use the following commands:\n'
        '/start - Start the bot\n'
        '/add - Add a new task\n'
        '/view - View all tasks\n'
        '/delete - Delete a task\n'
        '/help - Show this help message'
    )

def add(update: Update, context: CallbackContext) -> None:
    task = ' '.join(context.args)
    add_task(task)
    update.message.reply_text(f"Task '{task}' added!")

def view(update: Update, context: CallbackContext) -> None:
    tasks = get_tasks()
    if tasks:
        update.message.reply_text('\n'.join([f"{task[0]}. {task[1]}" for task in tasks]))
    else:
        update.message.reply_text("No tasks found.")

def delete(update: Update, context: CallbackContext) -> None:
    try:
        task_id = int(context.args[0])
        delete_task(task_id)
        update.message.reply_text(f"Task {task_id} deleted!")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /delete <task_id>")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'You can use the following commands:\n'
        '/start - Start the bot\n'
        '/add - Add a new task\n'
        '/view - View all tasks\n'
        '/delete - Delete a task\n'
        '/help - Show this help message'
    )

# Функция для запуска бота
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрация обработчиков команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("view", view))
    dp.add_handler(CommandHandler("delete", delete))
    dp.add_handler(CommandHandler("help", help_command))

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запуск APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(run_bot, 'interval', seconds=10)
scheduler.start()

# Запуск Flask
@app.route('/')
def index():
    return "Hello, this is the Task Tracker bot!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
