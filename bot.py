import telebot
from telebot import types
import sqlite3
import os

# Telegram bot token
TOKEN = "6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg"
bot = telebot.TeleBot(TTOKEN)

# Database setup
conn = sqlite3.connect('task_tracker.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task TEXT NOT NULL
)
''')
conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Task Tracker Bot! Use /help to see available commands.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "/start - Start the bot\n"
        "/help - Get help on how to use the bot\n"
        "/addtask - Add a new task\n"
        "/showtasks - Show all tasks\n"
        "/deletetask - Delete a task by ID"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['addtask'])
def add_task(message):
    msg = bot.reply_to(message, "Please send me the task description.")
    bot.register_next_step_handler(msg, save_task)

def save_task(message):
    user_id = message.from_user.id
    task = message.text
    cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)', (user_id, task))
    conn.commit()
    bot.reply_to(message, "Task added successfully!")

@bot.message_handler(commands=['showtasks'])
def show_tasks(message):
    user_id = message.from_user.id
    cursor.execute('SELECT id, task FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    if tasks:
        response = "\n".join([f"{task[0]}. {task[1]}" for task in tasks])
    else:
        response = "You have no tasks."
    bot.reply_to(message, response)

@bot.message_handler(commands=['deletetask'])
def delete_task(message):
    msg = bot.reply_to(message, "Please send me the ID of the task you want to delete.")
    bot.register_next_step_handler(msg, remove_task)

def remove_task(message):
    task_id = message.text
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    bot.reply_to(message, "Task deleted successfully!")

if __name__ == "__main__":
    bot.polling(none_stop=True)
