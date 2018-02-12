# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/komnaty/sdam/na_dlitelnyy_srok?pmin=11000&s=104&user=1&metro=157-160-163-165-176-180-191-199-201-202-205-206-210-1015-1016&f=512_5304-5305-5306-5307.583_14047b14049&i=1

AVITO_RSS = "http://avito2rss.bitcheese.net/feeds/7663.atom"
import feedparser


def get_avito_feed():
    d = feedparser.parse(AVITO_RSS)
    return [(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries[:10]]
