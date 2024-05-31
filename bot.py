from flask import Flask, send_from_directory, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import sqlite3
import json
import logging
import os
import threading

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Прямое указание токена
TOKEN = '6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        task TEXT,
        category TEXT,
        priority TEXT,
        notes TEXT
    )''')
    conn.commit()
    conn.close()

# Добавление задачи в базу данных
def add_task(user_id, task, category, priority, notes=''):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, task, category, priority, notes) VALUES (?, ?, ?, ?, ?)',
                   (user_id, task, category, priority, notes))
    conn.commit()
    conn.close()
    logger.info(f'Задача "{task}" добавлена пользователем {user_id}')

# Получение задач пользователя
def get_tasks(user_id):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT task, category, priority, notes FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Команда /start получена")
    keyboard = [
        [InlineKeyboardButton("Добавить задачу", web_app=WebAppInfo(url="https://my-unique-task-tracker-webapp-3bea140f1e44.herokuapp.com/"))],
        [InlineKeyboardButton("Показать задачи", callback_data='show_tasks')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я бот для управления Task Tracker. Выберите опцию:', reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    logger.info(f"Нажата кнопка с данными: {data}")

    if data == 'show_tasks':
        tasks = get_tasks(user_id)
        if tasks:
            response = 'Ваши задачи:\n' + '\n'.join([f'{task} [{category}] - приоритет: {priority}, заметки: {notes}' for task, category, priority, notes in tasks])
        else:
            response = 'У вас нет задач.'
        await query.message.reply_text(response)
    query.answer()

# Обработка данных из мини-приложения
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    data = json.loads(update.message.web_app_data.data)
    logger.info(f"Получены данные из мини-программы: {data}")

    task = data.get('task')
    category = data.get('category', 'Без категории')
    priority = data.get('priority', 'Средний')
    notes = data.get('notes', '')

    add_task(user.id, task, category, priority, notes)
    await update.message.reply_text(f'Задача "{task}" добавлена!')

def start_bot():
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    logger.info("Запуск бота")
    application.run_polling()

# Flask сервер для обслуговування статичних файлів з React
app = Flask(__name__, static_folder='client/build')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    user_id = request.args.get('user_id', type=int)
    tasks = get_tasks(user_id)
    return json.dumps(tasks)

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    data = request.json
    user_id = data['user_id']
    task = data['task']
    category = data['category']
    priority = data['priority']
    notes = data.get('notes', '')
    add_task(user_id, task, category, priority, notes)
    return json.dumps({'success': True})

if __name__ == "__main__":
    # Инициализация базы данных
    init_db()

    # Запуск Flask приложения в отдельном потоке
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    # Запуск Telegram бота
    start_bot()
