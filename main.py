from telegram.ext import Updater, CommandHandler
import logging
from config import TG_TOKEN, VK_PUBLICS_LIST
from vk_module import get_public_updates
from processing_module import process_text
from sql_module import execute_query

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
post_link = "https://vk.com/wall-{public_id}_{post_id}"

updater = Updater(token=TG_TOKEN)
dispatcher = updater.dispatcher
logger = updater.logger


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Привет, я буду присылать новые \nкомнаты в центре, подписывайся на рассылку.")


def parse_vk(bot, update):
    wall_data = []
    logger.info("Start parsing")
    for public_id in VK_PUBLICS_LIST:
        wall_data += get_public_updates(public_id, 10)
    logger.info("End parsing")
    for post in wall_data:
        timestamp = post['date'] * 1000
        text = post['text']
        public_id = -post['from_id']
        post_id = post['id']
        md5 = process_text(text)
        if md5:
            available_hashes = {a[0] for a in execute_query("SELECT md5 FROM hashes")}
            if md5 not in available_hashes:
                bot.send_message(chat_id=update.message.chat_id,
                                 text=post_link.format(public_id=public_id, post_id=post_id))
                execute_query("INSERT INTO hashes VALUES (?, ?)", (md5, timestamp))
        else:
            logger.info(f"{post_id} is not center room")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('parse', parse_vk))
updater.start_polling()
