from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import sqlite3

# Ваш токен бота
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
    keyboard = [
        [InlineKeyboardButton("Додати задачу", web_app=WebAppInfo(url="https://my-unique-task-tracker-webapp-3bea140f1e44.herokuapp.com/"))],
        [InlineKeyboardButton("Показати задачі", callback_data='show_tasks')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привіт! Я бот для управління Task Tracker. Виберіть опцію:', reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    if data == 'show_tasks':
        tasks = get_tasks(user_id)
        if tasks:
            response = 'Ваші задачі:\n' + '\n'.join([f'{task} [{category}] - пріоритет: {priority}, нотатки: {notes}' for task, category, priority, notes in tasks])
        else:
            response = 'У вас немає задач.'
        await query.message.reply_text(response)
    query.answer()

# Обработка данных из мини-приложения
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    data = update.message.web_app_data.data

    # Здесь можно обработать данные и добавить задачу в базу данных
    await update.message.reply_text(f'Отримані дані: {data}')

def main() -> None:
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    application.run_polling()

if __name__ == '__main__':
    main()
