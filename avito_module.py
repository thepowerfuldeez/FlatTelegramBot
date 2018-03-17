# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok/1-komnatnye?pmax=24000&pmin=18000&s=104&user=1&metro=154-155-156-158-161-163-167-173-177-178-179-181-184-185-187-188-189-194-211-2122&f=568_14010b14012&i=1

AVITO_RSS = "http://avito2rss.bitcheese.net/feeds/8129.atom"
import feedparser


def get_avito_feed():
    d = feedparser.parse(AVITO_RSS)
    return [(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries[:10]]
