import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import sqlite3
import pytz

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '6779858745:AAGBz3-5uSerXDXHYPVp1IgySy2yYJh3ueg'
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)

# Initialize updater and dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context) -> None:
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')

def help_command(update: Update, context) -> None:
    update.message.reply_text('Help!')

def alarm(context) -> None:
    job = context.job
    context.bot.send_message(job.context, text='Beep!')

def set_timer(update: Update, context) -> None:
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry, we can not go back to future!')
            return

        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        update.message.reply_text(f'Timer successfully set for {due} seconds!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def button(update: Update, context) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    updater.dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return 'Hello, I am your bot!'

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f"https://{os.environ.get('HEROKU_APP_NAME')}.herokuapp.com/{TOKEN}")
    updater.idle()
