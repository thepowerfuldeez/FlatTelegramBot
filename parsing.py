#1. Loading BeautifulSoup and test request
from bs4 import BeautifulSoup
import requests
import re

# CIAN_URL = "https://www.cian.ru/cat.php?currency=2&engine_version=2&offer_type=flat&totime=86400"
CIAN_URL = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&foot_min=15&metro%5B0%5D=1&metro%5B10%5D=37&metro%5B11%5D=53&metro%5B12%5D=61&metro%5B13%5D=66&metro%5B14%5D=83&metro%5B15%5D=91&metro%5B16%5D=95&metro%5B17%5D=103&metro%5B18%5D=107&metro%5B19%5D=110&metro%5B1%5D=5&metro%5B20%5D=116&metro%5B21%5D=117&metro%5B22%5D=128&metro%5B23%5D=134&metro%5B24%5D=155&metro%5B25%5D=236&metro%5B26%5D=237&metro%5B27%5D=286&metro%5B28%5D=287&metro%5B29%5D=296&metro%5B2%5D=9&metro%5B30%5D=351&metro%5B3%5D=13&metro%5B4%5D=14&metro%5B5%5D=15&metro%5B6%5D=21&metro%5B7%5D=27&metro%5B8%5D=28&metro%5B9%5D=36&minarea=38&offer_type=flat&only_foot=2&totime=86400"
# AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?cd=1&s=104&f=ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk"
AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?cd=1&s=104&metro=1-7-10-11-12-13-19-21-23-30-31-48-49-57-66-73-78-85-89-91-97-101-102-104-110-111-121-126-139-144-151-2001-2002-2154-2155-2157-2193-2195&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUjlkBRfAIGHsiZnJvbSI6MTQwMTEsInRvIjpudWxsfQ"

def get_cian_url(deal_type='rent', minprice=35000, maxprice=55000, number_of_rooms=1, region=1, page=1):
    return f"{CIAN_URL}&region={region}&deal_type={deal_type}&minprice={minprice}&maxprice={maxprice}&room1=1&p={page}"

def get_avito_url(minprice=35000, maxprice=55000, page=1):
    return f"{AVITO_URL}&pmin={minprice}&pmax={maxprice}&p={page}"
       
def get_cian_feed():
    url = get_cian_url()
    cian_html = requests.get(url).text
    soup = BeautifulSoup(cian_html)

    flats_items = []
    flats = soup.find_all('div', {'data-name': re.compile('OfferCard')})
    for f in flats:
        flat_imgs = []

        additional_imgs = f.find_all('img', {'data-name': 'GalleryImage'})
        if additional_imgs:
            flat_imgs.append(f.find('img')['src'])

        for fa in additional_imgs:
            flat_imgs.append(fa['src'])

        links = f.find_all('a', {'target': '_blank'})
        for a in links:
            if 'https://www.cian.ru/rent/flat/' or 'https://www.cian.ru/sale/flat/' in a['href']:
                if '/cat.php?' not in a['href'] and flat_imgs:
                    flats_items.append({"link": a['href'], "photos": list(set(flat_imgs))})
                    break

    return flats_items
    

def get_avito_feed():
    url = get_avito_url()
    avito_html = requests.get(url).text
    soup = BeautifulSoup(avito_html)

    flats_items = []
    flats = soup.find_all('a', {'class': 'js-item-slider item-slider'})
        
    for f in flats:
        flat_imgs = []
        link = f['href']
        
        imgs = f.find_all('img', {'class': 'large-picture-img'})
        for img in imgs:
            if img.has_attr('srcset'):
                flat_imgs.append(img['srcset'].split()[-2])
            elif img.has_attr('data-srcset'):
                flat_imgs.append(img['data-srcset'].split()[-2])

        if 'kvartiry/' in link and flat_imgs:
            flats_items.append({"link": f"https://avito.ru{link}", "photos": list(set(flat_imgs))})

    return flats_items
