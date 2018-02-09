# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/komnaty/sdam/na_dlitelnyy_srok?pmax=13000&pmin=8000&s=104&user=1&metro=157-160-165-176-180-191-199-201-202-205-206-210-1015-1016-2132&f=512_5305-5306.583_14047b

AVITO_RSS = "http://avito2rss.bitcheese.net/feeds/7638.atom"
import feedparser


def get_avito_feed():
    d = feedparser.parse(AVITO_RSS)
    return [(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries]
