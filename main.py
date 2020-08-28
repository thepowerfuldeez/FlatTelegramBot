import logging
import time
import datetime
import uuid
import json
from pathlib import Path

import cv2
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
OUT_DIR = Path("/root/FlatTelegramBot/logs")


REQUEST_KWARGS={
    'proxy_url': 'socks5://78.47.225.59:9050',
    'connect_timeout': 15.,
    'read_timeout': 15.
}


def send_message(bot, link):
    bot.send_message(chat_id="@instantflats",
                     text=link)
    db.update(link)
    
    

def process_photos(photos, save_images=True):
    """Process and infer one item from cian/avito feed, 
    return confidence of good looking flat"""
    confidences = []
    images = []
    for photo_link in photos:
        im = pseudo_download_img(photo_link)
        if min(im.shape[:2]) < 128:
            continue
        _, good_prob = get_prediction(im)
        confidences.append(good_prob)
        if save_images:
            images.append(im)
    
    return confidences, images
    

def save_logs(out_dir, item, images, confidences):
    out_dir.mkdir(exist_ok=True, parents=True)
    with open(out_dir/"result.json", "w") as f:
        result = {"link": item['link'], "price": item.get('price'), "images": []}
        for i in range(1, len(images)+1):
            cv2.imwrite(str(out_dir/f"{i}.jpg"), images[i-1][...,::-1])
            result['images'].append({'name': f"{i}.jpg", "confidence": float(confidences[i-1])})
        json.dump(result, f)
    print('saved logs for', item)



def cian_job(context: telegram.ext.CallbackContext):
    logger.info("Start parsing cian")
    feed = get_cian_feed()
    for item in feed:
        link = item['link']
        if link not in db:
            # item has many photos
            confidences, images = process_photos(item['photos'])
            item_result = max(confidences)
            logger.info(f"item result is {item_result}")
            if item_result > THRESHOLD_CIAN:
                send_message(context.bot, f"{item.get('price')} {link}")
            db.update(link)
            
            try:
                save_logs(OUT_DIR/"cian"/uuid.uuid4().hex, item, images, confidences)
            except Exception as e: print(e)
    logger.info("End parsing cian")
        

def avito_job(context: telegram.ext.CallbackContext):
    logger.info("Start parsing avito")
    feed = get_avito_feed()
    for item in feed:
        link = item['link']
        if link not in db:
            confidences, images = process_photos(item['photos'])
            item_result = max(confidences)
            logger.info(f"item result is {item_result}")
            if item_result > THRESHOLD_AVITO:
                send_message(context.bot, item['link'])
            db.update(item['link'])

        try:
            save_logs(OUT_DIR/"avito"/uuid.uuid4().hex, item, images, confidences)
        except Exception as e: print(e)
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


