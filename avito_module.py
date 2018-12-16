# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?f=550_5702-5703&metro=156-158-163-164-173-185-189-194-201-202-203-209-211-1015-2197&s=104&s_trg=3&user=1

AVITO_RSS_ARRAY = ["https://avito2rss.duck.consulting/feeds/13825.atom",
                   "https://avito2rss.duck.consulting/feeds/13826.atom"]
import feedparser
import time


def get_avito_feed():
    feed = []
    for avito_rss in AVITO_RSS_ARRAY:
        d = feedparser.parse(avito_rss)
        feed.extend([{
            "title": entry.title,
            "link": entry.link,
            "text": entry.content[0].value,
            "updated": entry.updated
        } for entry in d.entries[:10]])
        time.sleep(0.5)
    return feed


if __name__ == "__main__":
    feed = get_avito_feed()
    print(feed[0])
