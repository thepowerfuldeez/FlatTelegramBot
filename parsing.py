#1. Loading BeautifulSoup and test request
from bs4 import BeautifulSoup
import requests
import re

CIAN_URL = "https://www.cian.ru/cat.php?currency=2&engine_version=2&offer_type=flat&totime=86400"
AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?cd=1&s=104&f=ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk"

def get_cian_url(deal_type='rent', minprice=30000, maxprice=50000, number_of_rooms=1, region=1, page=1):
    return f"{CIAN_URL}&region={region}&deal_type={deal_type}&minprice={minprice}&maxprice={maxprice}&room1=1&p={page}"

def get_avito_url(minprice=30000, maxprice=50000, page=1):
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
