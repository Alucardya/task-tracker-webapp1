from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import sqlite3
import json
import logging
import os

# Логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш токен бота
TOKEN = '6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg'

# Назва вашого Heroku додатка
HEROKU_APP_NAME = 'my-unique-task-tracker-webapp-3bea140f1e44'

# Ініціалізація бази даних
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

# Додавання задачі до бази даних
def add_task(user_id, task, category, priority, notes=''):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, task, category, priority, notes) VALUES (?, ?, ?, ?, ?)',
                   (user_id, task, category, priority, notes))
    conn.commit()
    conn.close()
    logger.info(f'Задача "{task}" додана користувачем {user_id}')

# Отримання задач користувача
def get_tasks(user_id):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT task, category, priority, notes FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Обробка команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Команда /start отримана")
    keyboard = [
        [InlineKeyboardButton("Додати задачу", web_app=WebAppInfo(url=f"https://{HEROKU_APP_NAME}.herokuapp.com/"))],
        [InlineKeyboardButton("Показати задачі", callback_data='show_tasks')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привіт! Я бот для управління Task Tracker. Виберіть опцію:', reply_markup=reply_markup)

# Обробка натискань на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    logger.info(f"Натиснута кнопка з даними: {data}")

    if data == 'show_tasks':
        tasks = get_tasks(user_id)
        if tasks:
            response = 'Ваші задачі:\n' + '\n'.join([f'{task} [{category}] - пріоритет: {priority}, нотатки: {notes}' for task, category, priority, notes in tasks])
        else:
            response = 'У вас немає задач.'
        await query.message.reply_text(response)
    await query.answer()

# Обробка даних з міні-програми
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    data = json.loads(update.message.web_app_data.data)
    logger.info(f"Отримані дані з міні-програми: {data}")

    task = data.get('task')
    category = data.get('category', 'Без категорії')
    priority = data.get('priority', 'Середній')
    notes = data.get('notes', '')

    add_task(user.id, task, category, priority, notes)
    await update.message.reply_text(f'Задача "{task}" додана!')

def main() -> None:
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    logger.info("Запуск бота")

    # Налаштування вебхука
    PORT = int(os.environ.get('PORT', '8443'))
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}"
    )

if __name__ == '__main__':
    main()
