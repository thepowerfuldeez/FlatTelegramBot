# Using http://avito2rss.bitcheese.net
# avito link – https://www.avito.ru/sankt-peterburg/sport_i_otdyh/drugoe?s=104&user=1&q=электросамокат+xiaomi

AVITO_RSS = "http://avito2rss.bitcheese.net/feeds/8584.atom"
import feedparser


def get_avito_feed():
    d = feedparser.parse(AVITO_RSS)
    return [(entry.title, entry.link, entry.content[0].value, entry.updated) for entry in d.entries[:15]]
