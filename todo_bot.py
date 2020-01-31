import os
import logging
from dotenv import load_dotenv
from telegram import Bot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("echo-bot")

max_id = 0


def main():
    global max_id
    load_dotenv()
    token = os.environ.get("ACCESS_TOKEN")
    bot = Bot(token)
    while True:
        logger.debug("start request")
        # Мы хотим получать только новые апдейты, поэтому мы завели переменную max_id
        # и вызываем метод getUpdates с параметром offset + timeout
        updates = bot.getUpdates(offset=max_id + 1, timeout=60)
        # В этой переменной мы сохраним максимальный id из полученных сейчас updates
        max_id_in_updates = 0
        for upd in updates:
            logger.debug(f"new update with id: {upd.update_id}")
            # Может быть так, что запустив бота мы получим апдейты
            # которые произошли во время его "спячки", мы их просто отфильтруем следующим условием
            # потому как max_id будет изменен только после обработки первых апдейтов
            if max_id != 0:
                bot.sendMessage(
                    upd.message.chat_id,
                    upd.message.text,
                    reply_to_message_id=upd.message.message_id,
                )
            max_id_in_updates = (
                upd.update_id
                if upd.update_id > max_id_in_updates
                else max_id_in_updates
            )
        if max_id_in_updates and max_id != max_id_in_updates:
            max_id = max_id_in_updates
            logger.debug(f"max id is changed to {max_id_in_updates}")


if __name__ == "__main__":
    main()
