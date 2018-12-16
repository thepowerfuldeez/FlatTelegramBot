from telegram.ext import Updater, CommandHandler
import logging
import os
import time
import datetime
from vk_module import get_public_updates
from avito_module import get_avito_feed
from processing_module import process_text_vk, process_text_avito
from config import TG_TOKEN
from data import db, check_duplicates, IMG_PATH, save_img

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
post_link = "https://vk.com/wall-{public_id}_{post_id}"
VK_PUBLICS_LIST = [57466174, 133717012, 1850339, 90529595, 12022371, 126712296, 150611459, 1744988, 28618880, 27701671,
                   35098427]

REQUEST_KWARGS={
    'proxy_url': 'socks5://78.47.225.59:9050',
    'connect_timeout': 15.,
    'read_timeout': 15.
}

# https://vk.com/topic-12022371_36100298?offset=300
# https://vk.com/topic-90529595_34531077?offset=1400
# https://vk.com/topic-150611459_35921948?offset=340
# https://vk.com/topic-1744988_21328151?offset=30300
# https://vk.com/topic-28618880_36966519?offset=100
# https://vk.com/topic-27701671_24755429?offset=15460


def send_messages(bot):
    for post in db.flats.find({'sent': False}):
        bot.send_message(chat_id="@instantflats",
                         text=post['link'])
        db.flats.update_one({"text": post['text']}, {"$set": {"sent": True}})
        time.sleep(0.5)


def parse_vk(bot, update):
    wall_data = []
    logger.info("Start parsing vk")
    for public_id in VK_PUBLICS_LIST:
        wall_data += get_public_updates(public_id, 10)
        time.sleep(0.5)
    logger.info("End parsing vk")
    for post in wall_data:
        if 'attachments' in post:
            print([item.keys() for item in post['attachments']])
            img_links = [item.get('photo_604', "") for item in post['attachments'] if item['type'] == "photo"]
            img_links = list(filter(lambda x: x != "", img_links))
            if len(img_links):
                timestamp = post['date'] * 1000
                text = post['text']
                public_id = -post['from_id']
                post_id = post['id']
                s = process_text_vk(text)
                if s and db.flats.find({"text": s}).limit(1).count() == 0:
                    post_id = db.flats.insert_one({
                        "text": s,
                        "link": f"https://vk.com/wall-{public_id}_{post_id}",
                        "from": "vk",
                        "sent": False,
                    }).inserted_id
                    img_paths = [save_img(link) for link in img_links]
                else:
                    logger.info(f"{post_id} is not center room")
    send_messages(bot)


def parse_avito(bot, update):
    logger.info("Start parsing avito")
    feed = get_avito_feed()
    for item in feed:
        s = process_text_avito(item['text'])

        date = datetime.datetime.strptime(item['updated'], "%Y-%m-%dT%H:%M:%SZ")
        timestamp = int(date.timestamp())
        timedelta = datetime.datetime.now() - date
        if s and timedelta.days < 1 and check_duplicates(s):
            post_id = db.flats.insert_one({
                "text": s,
                "link": item['link'],
                "from": "avito",
                "sent": False,
            }).inserted_id
            img_paths = [save_img(link) for link in item['img_links']]
    logger.info("End parsing avito")
    send_messages(bot)


def main():
    print("history count", db.history.count())
    updater = Updater(TG_TOKEN, request_kwargs=REQUEST_KWARGS)
    job_queue = updater.job_queue
    job_queue.run_repeating(parse_vk, interval=360, first=0)
    job_queue.run_repeating(parse_avito, interval=600, first=0)
    job_queue.start()


if __name__ == '__main__':
    main()


