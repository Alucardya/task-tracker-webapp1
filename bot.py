import os
import sqlite3
from flask import Flask, send_from_directory, render_template
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import pytz

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask application setup
app = Flask(__name__, static_folder='task-tracker-client/build')

# Retrieve the Telegram bot token from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError('`TELEGRAM_BOT_TOKEN` must be set as an environment variable')
bot = Bot(token=TOKEN)

# SQLite database functions
def init_db():
    db_path = os.path.join(os.getcwd(), 'task_tracker.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
    conn.commit()
    conn.close()

def add_task(task):
    db_path = os.path.join(os.getcwd(), 'task_tracker.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def get_tasks():
    db_path = os.path.join(os.getcwd(), 'task_tracker.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    db_path = os.path.join(os.getcwd(), 'task_tracker.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Telegram bot command handlers
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

# Function to run the Telegram bot
def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("view", view))
    dp.add_handler(CommandHandler("delete", delete))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

# APScheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(run_bot, IntervalTrigger(seconds=10, timezone=pytz.utc))
scheduler.start()

# Flask routes to serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
