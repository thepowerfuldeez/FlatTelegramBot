#1. Loading BeautifulSoup and test request
from bs4 import BeautifulSoup
import requests
import re

from config import SCRAPINGBEE_API_KEY

# CIAN_URL = "https://www.cian.ru/cat.php?currency=2&engine_version=2&offer_type=flat&totime=86400"
CIAN_URL = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&foot_min=15&minarea=35&offer_type=flat&only_foot=2&region=1&room1=1&room9=1&totime=3600&type=4"
# AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?cd=1&s=104&f=ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk"
AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?cd=1&s=104&metro=1-4-6-7-10-11-12-13-16-18-19-21-23-25-30-31-32-42-45-48-49-50-52-54-57-60-62-64-66-72-73-75-79-80-82-85-89-90-91-92-97-99-101-102-104-108-110-111-114-116-117-118-121-122-124-126-134-137-138-139-144-151-1006-1007-2001-2002-2154-2155-2157-2193-2194-2195&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUjlkBRfAIGHsiZnJvbSI6MTQwMTAsInRvIjpudWxsfQ"

def get_cian_url(deal_type='rent', minprice=35000, maxprice=55000, number_of_rooms=1, region=1, page=1):
    return CIAN_URL
    #return f"{CIAN_URL}&region={region}&deal_type={deal_type}&minprice={minprice}&maxprice={maxprice}&room1=1&p={page}"

def get_avito_url(minprice=35000, maxprice=55000, page=1):
    return AVITO_URL
    #return f"{AVITO_URL}&pmin={minprice}&pmax={maxprice}&p={page}"
       
def get_cian_feed():
    url = get_cian_url()
    cian_html = requests.get(
            url="https://app.scrapingbee.com/api/v1/",
            params={
        "api_key": SCRAPINGBEE_API_KEY,
        "url": url, 
        "render_js": "false"
        }).text
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
    avito_html = requests.get(
            url="https://app.scrapingbee.com/api/v1/",
            params={
        "api_key": SCRAPINGBEE_API_KEY,
        "url": url,
        "render_js": "false",
        }).text
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
