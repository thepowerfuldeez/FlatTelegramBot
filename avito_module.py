# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok/1-komnatnye?pmax=25000&pmin=17000&s=104&user=1&metro=161-163-177-178-179-184-187-188-2122&f=568_14009b14012&i=1

AVITO_RSS = "http://avito2rss.bitcheese.net/feeds/8127.atom"
import feedparser


def get_avito_feed():
    d = feedparser.parse(AVITO_RSS)
    return [(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries[:10]]
