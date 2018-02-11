from telegram.ext import Updater, CommandHandler
import logging
import os
import datetime
from vk_module import get_public_updates
from avito_module import get_avito_feed
from processing_module import process_text_vk, process_text_avito
from sql_module import execute_query

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
post_link = "https://vk.com/wall-{public_id}_{post_id}"
VK_PUBLICS_LIST = [57466174, 133717012, 1850339, 90529595, 12022371]


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Привет, я буду присылать новые \nкомнаты в центре, подписывайся на рассылку.")

def send_message_and_update(bot, text, md5, timestamp):
    available_hashes = {a[0] for a in execute_query("SELECT md5 FROM hashes")}
    if md5 not in available_hashes:
        bot.send_message(chat_id="@instantflats",
                         text=text)
        execute_query("INSERT INTO hashes VALUES (?, ?)", (md5, timestamp))


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
        md5 = process_text_vk(text)
        if md5:
            send_message_and_update(bot, post_link.format(public_id=public_id, post_id=post_id), md5, timestamp)
        else:
            logger.info(f"{post_id} is not center room")


def parse_avito(bot, update):
    rss = get_avito_feed()
    for title, link, text, timestring in rss:
        md5 = process_text_avito(text)
        date = datetime.datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
        timestamp = int(date.timestamp())
        timedelta = datetime.datetime.now() - date
        if md5 and timedelta.days < 1:
            send_message_and_update(bot, f"{title}\n{link}", md5, timestamp)


def main():
    updater = Updater(token=os.environ.get("TG_TOKEN"))
    job_queue = updater.job_queue
    job_queue.run_repeating(parse_vk, interval=360, first=0)
    job_queue.run_repeating(parse_avito, interval=360, first=0)
    job_queue.start()


if __name__ == '__main__':
    main()
