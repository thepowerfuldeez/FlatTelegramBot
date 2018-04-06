from telegram.ext import Updater, CommandHandler
import logging
import os
import time
import datetime
from vk_module import get_public_updates
from avito_module import get_avito_feed
from processing_module import process_text_vk, process_text_avito
from sql_module import execute_query

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


def send_message_and_update(bot, text, md5, timestamp):
    available_hashes = {a[0] for a in execute_query("SELECT md5 FROM hashes")}
    if md5 not in available_hashes:
        bot.send_message(chat_id="@instantflats",
                         text=text)
        execute_query("INSERT INTO hashes VALUES (?, ?)", (md5, timestamp))
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
    # job_queue.run_repeating(parse_vk, interval=360, first=0)
    job_queue.run_repeating(parse_avito, interval=720, first=180)
    job_queue.start()


if __name__ == '__main__':
    main()


