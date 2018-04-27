# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/sport_i_otdyh/drugoe?s=104&user=1&q=электросамокат+xiaomi

AVITO_RSS_ARRAY = ["http://avito2rss.bitcheese.net/feeds/8871.atom",
                   "http://avito2rss.bitcheese.net/feeds/8872.atom",
                   "http://avito2rss.bitcheese.net/feeds/8873.atom",
                   "http://avito2rss.bitcheese.net/feeds/8883.atom",
                   "http://avito2rss.bitcheese.net/feeds/8884.atom",
                   "http://avito2rss.bitcheese.net/feeds/8885.atom",
                   "http://avito2rss.bitcheese.net/feeds/8886.atom"]
import feedparser
import time


def get_avito_feed():
    feed = []
    for i, AVITO_RSS in enumerate(AVITO_RSS_ARRAY):
        d = feedparser.parse(AVITO_RSS)
        if i > 2:
            feed.extend([("МСК " + entry.title, entry.link, entry.content[0].value, entry.updated)
                         for entry in d.entries[:5]])
        time.sleep(0.5)
    return feed
