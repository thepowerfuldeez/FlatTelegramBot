#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vkstreaming import getServerUrl, Streaming
from config import SERVICE_TOKEN, TG_TOKEN
from data import db, check_duplicates
from processing_module import process_text_vk


response = getServerUrl(SERVICE_TOKEN)
api = Streaming("streaming.vk.com", response['key'])

api.del_all_rules()
api.add_rules(f"rule_1", "квартира снимать комната спб")
api.add_rules(f"rule_2", "квартира сдавать комната спб")
api.add_rules(f"rule_3", "квартира сдам комната спб")

print("currently", len(api.get_rules()), "rules loaded")


@api.stream
def my_func(event):
    event_text = event['text']
    if "attachments" in event:
        # img_links = [item['photo_link'] for item in event['attachments']]
        s = process_text_vk(event_text)
        if s and check_duplicates(s):
            print("adding new event")
            post_id = db.flats.insert_one({
                "text": s,
                "link": event['event_url'],
                "from": "vk_streaming",
                "sent": False,
            }).inserted_id


    # if event['event_type'] == "post":
    #     event_text = event['text']
    #     event_link = event['event_url']
    #     event_date = event['date']
    #     if "attachments" in event:
    #         for a in event["attachments"]:
    #             if a['type'] == "link":
    #                 event_link = a['link']
    #                 try:
    #                     end_sent = event_text.find(".")
    #                     if end_sent < 5 or end_sent > 60:
    #                         end_sent = max(20, len(" ".join(event_text.split()[:3])))
    #                     event_title = event_text[:end_sent + 1]
    #                 except:
    #                     event_title = None
    #
    #                 event_city = extract_city(event_text)
    #                 post_vector = enc.get_post_vector(text=event_text)
    #                 if np.isnan(post_vector.sum()):
    #                     post_vector = np.zeros(200)
    #                 prob = mlp_event_.predict_proba(post_vector.reshape(1, -1))[0][1]
    #                 print(event_text[-50:], event_link, event_city, prob)
    #                 if prob > 0.35:
    #                     print(event_title)
    #                     data.EVENTS.append(Event(
    #                         description=event_text, city=event_city, title=event_title,
    #                         link=event_link, vector=post_vector, date=event_date
    #                     ))


api.start()
