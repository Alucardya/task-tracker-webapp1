from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Ваш токен бота
TOKEN = '6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg'

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    if data == 'show_tasks':
        # Обработка показа задач здесь
        await query.message.reply_text('Ваши задачи: ...')

# Обработка данных из мини-приложения
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    data = update.message.web_app_data.data

    # Здесь можно обработать данные и добавить задачу в базу данных
    await update.message.reply_text(f'Получены данные: {data}')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    application.run_polling()

if __name__ == '__main__':
    main()
