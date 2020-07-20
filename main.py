import logging
import time
import datetime

import telegram.ext
from telegram.ext import Updater, CommandHandler

from inference.demo import get_prediction
from parsing import get_avito_feed, get_cian_feed
from download_lib import pseudo_download_img
from db import DB
from config import TG_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

db = DB("seen_links.json")

THRESHOLD_AVITO = 0.5
THRESHOLD_CIAN = 0.6


REQUEST_KWARGS={
    'proxy_url': 'socks5://78.47.225.59:9050',
    'connect_timeout': 15.,
    'read_timeout': 15.
}


def send_message(bot, link):
    bot.send_message(chat_id="@instantflats",
                     text=link)
    db.update(link)
    
    

def process_photos(photos):
    """Process and infer one item from cian/avito feed, 
    return confidence of good looking flat"""
    confidences = []
    for photo_link in photos:
        im = pseudo_download_img(photo_link)
        if min(im.shape[:2]) < 128:
            continue
        _, good_prob = get_prediction(im)
        confidences.append(good_prob)
    
    return max(confidences)
    


def cian_job(context: telegram.ext.CallbackContext):
    logger.info("Start parsing cian")
    feed = get_cian_feed()
    for item in feed:
        link = item['link']
        if link not in db:
            # item has many photos
            item_result = process_photos(item['photos'])
            logger.info(f"item result is {item_result}")
            if item_result > THRESHOLD_CIAN:
                send_message(context.bot, f"{item.get('price')} {link}")
            db.update(link)
    logger.info("End parsing cian")
        

def avito_job(context: telegram.ext.CallbackContext):
    logger.info("Start parsing avito")
    feed = get_avito_feed()
    for item in feed:
        link = item['link']
        if link not in db:
            item_result = process_photos(item['photos'])
            logger.info(f"item result is {item_result}")
            if item_result > THRESHOLD_AVITO:
                send_message(context.bot, item['link'])
            db.update(item['link'])
    logger.info("End parsing avito")


def main():
    logger.info("starting to work")
    updater = Updater(TG_TOKEN, use_context=True)#, request_kwargs=REQUEST_KWARGS)
    job_queue = updater.job_queue
    job_queue.run_repeating(cian_job, interval=3600, first=0)
    job_queue.run_repeating(avito_job, interval=3600, first=0)
    job_queue.start()


if __name__ == '__main__':
    main()


