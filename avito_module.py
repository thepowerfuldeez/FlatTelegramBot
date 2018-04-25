# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/sport_i_otdyh/drugoe?s=104&user=1&q=электросамокат+xiaomi
# https://www.avito.ru/sankt-peterburg/sport_i_otdyh?s=104&user=1&q=Xiaomi+Mijia+Electric+Scooter


AVITO_RSS_ARRAY = ["http://avito2rss.bitcheese.net/feeds/8871.atom",
                   "http://avito2rss.bitcheese.net/feeds/8872.atom",
                   "http://avito2rss.bitcheese.net/feeds/8873.atom"]
import feedparser


def get_avito_feed():
    feed = []
    for AVITO_RSS in AVITO_RSS_ARRAY:
        d = feedparser.parse(AVITO_RSS)
        feed.extend([(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries[:5]])
    return feed
