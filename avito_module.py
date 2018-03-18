# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok?pmax=24000&pmin=18000&s=104&user=1&metro=154-155-156-158-161-162-163-167-171-173-177-178-179-181-184-185-186-187-188-189-194-211-1017-2122-2137-2138&f=550_5702-5703.568_14010b14012&i=1

AVITO_RSS = "http://avito2rss.bitcheese.net/feeds/8136.atom"
import feedparser


def get_avito_feed():
    d = feedparser.parse(AVITO_RSS)
    return [(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries[:15]]
