import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("echo-bot")


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
        reply_to_message_id=update.message.message_id,
    )


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")


def main():
    load_dotenv()
    token = os.environ.get("ACCESS_TOKEN")
    # Создаем экземпляр класса Updater
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    # Создаем 2 хендлера
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    # Начинаем запрашивать обновления от Telegram Bot API
    updater.start_polling()


if __name__ == "__main__":
    main()
