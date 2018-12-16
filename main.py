from telegram.ext import Updater, CommandHandler
import logging
import os
import time
import datetime
from vk_module import get_public_updates
from avito_module import get_avito_feed
from processing_module import process_text_vk, process_text_avito
from config import TG_TOKEN
from data import db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
post_link = "https://vk.com/wall-{public_id}_{post_id}"
VK_PUBLICS_LIST = [57466174, 133717012, 1850339, 90529595, 12022371, 126712296, 150611459, 1744988, 28618880, 27701671,
                   35098427]

# https://vk.com/topic-12022371_36100298?offset=300
# https://vk.com/topic-90529595_34531077?offset=1400
# https://vk.com/topic-150611459_35921948?offset=340
# https://vk.com/topic-1744988_21328151?offset=30300
# https://vk.com/topic-28618880_36966519?offset=100
# https://vk.com/topic-27701671_24755429?offset=15460


def send_message_and_update(bot, text, link, key):
    print(db.history.find({'text': text}).limit(1).count())
    if db.history.find({'text': text}).limit(1).count() == 0:
        bot.send_message(chat_id="@instantflats",
                         text=link)
        post_id = db.history.insert_one({"text": text, "link": link}).inserted_id
    time.sleep(1)


def parse_vk(bot, update):
    wall_data = []
    logger.info("Start parsing")
    for public_id in VK_PUBLICS_LIST:
        wall_data += get_public_updates(public_id, 10)
        time.sleep(0.5)
    logger.info("End parsing")
    for post in wall_data:
        timestamp = post['date'] * 1000
        text = post['text']
        public_id = -post['from_id']
        post_id = post['id']
        s = process_text_vk(text)
        if s:
            send_message_and_update(bot, s, post_link.format(public_id=public_id, post_id=post_id), "vk")
        else:
            logger.info(f"{post_id} is not center room")


def parse_avito(bot, update):
    rss = get_avito_feed()
    for title, link, text, timestring in rss:
        s = process_text_avito(text)
        date = datetime.datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
        timestamp = int(date.timestamp())
        timedelta = datetime.datetime.now() - date
        if s and timedelta.days < 1:
            send_message_and_update(bot, title, link, "avito")


def main():
    print("history count", db.history.count())
    updater = Updater(TG_TOKEN)
    job_queue = updater.job_queue
    job_queue.run_repeating(parse_vk, interval=360, first=0)
    job_queue.run_repeating(parse_avito, interval=600, first=0)
    job_queue.start()


if __name__ == '__main__':
    main()


