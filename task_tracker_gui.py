import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, Message
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Ваш токен бота
TOKEN = '6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        task TEXT,
        category TEXT,
        priority TEXT,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

# Добавление пользователя в базу данных
def add_user(user_id, username):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
    conn.close()

# Добавление задачи в базу данных
def add_task(user_id, task, category, priority, notes=''):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (user_id, task, category, priority, notes) VALUES (?, ?, ?, ?, ?)', (user_id, task, category, priority, notes))
    conn.commit()
    conn.close()

# Удаление задачи из базы данных
def delete_task(user_id, task):
    conn = sqlite3.connect('task_tracker.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE user_id = ? AND task = ?', (user_id, task))
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
    user = update.message.from_user
    add_user(user.id, user.username)
    keyboard = [
        [InlineKeyboardButton("Добавить задачу", callback_data='add_task')],
        [InlineKeyboardButton("Показать задачи", callback_data='show_tasks')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я бот для управления Task Tracker. Выберите опцию:', reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = query.from_user
    data = query.data

    if data == 'add_task':
        await query.message.reply_text('Введите задачу в формате: <текст задачи> #<категория> !<приоритет>')
        context.user_data['adding_task'] = True
    elif data == 'show_tasks':
        tasks = get_tasks(user.id)
        if tasks:
            response = 'Ваши задачи:\n' + '\n'.join([f'({priority}) {task} [{category}] - {notes}' for task, category, priority, notes in tasks])
            keyboard = [[InlineKeyboardButton(f"Удалить {task}", callback_data=f"delete_{task}")] for task, _, _, _ in tasks]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(response, reply_markup=reply_markup)
        else:
            await query.message.reply_text('У вас нет задач.')
    elif data.startswith("delete_"):
        task = data[len("delete_"):]
        delete_task(user.id, task)
        await query.edit_message_text(text=f'Задача "{task}" удалена.')
    context.user_data['adding_task'] = False

# Обработка текстовых сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text

    if context.user_data.get('adding_task'):
        parts = text.split()
        if len(parts) >= 1:
            task = parts[0]
            category = 'Inbox'
            priority = 'p4'
            notes = ''
            for part in parts[1:]:
                if part.startswith('#'):
                    category = part[1:]
                elif part.startswith('!'):
                    priority = part[1:]
                else:
                    notes += ' ' + part
            add_task(user.id, task, category, priority, notes.strip())
            await update.message.reply_text(f'Задача "{task}" добавлена в категорию "{category}" с приоритетом "{priority}".')
        context.user_data['adding_task'] = False

def main() -> None:
    # Инициализация базы данных
    init_db()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
