#1. Loading BeautifulSoup and test request
from bs4 import BeautifulSoup
import requests
import re

from config import SCRAPINGBEE_API_KEY

#CIAN_URL = "https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&in_polygon%5B1%5D=37.5656_55.7547%2C37.5653_55.7576%2C37.5651_55.7605%2C37.5654_55.7634%2C37.5666_55.7663%2C37.5687_55.769%2C37.5706_55.7719%2C37.573_55.7745%2C37.5754_55.7771%2C37.5787_55.7797%2C37.5814_55.7822%2C37.6272_55.7909%2C37.6324_55.791%2C37.6377_55.7911%2C37.643_55.7911%2C37.6482_55.7907%2C37.6532_55.7898%2C37.6569_55.7877%2C37.6593_55.7851%2C37.6623_55.7827%2C37.6638_55.7799%2C37.665_55.777%2C37.6671_55.7743%2C37.6703_55.7719%2C37.6714_55.769%2C37.672_55.7661%2C37.6732_55.7632%2C37.6741_55.7603%2C37.6743_55.7574%2C37.6743_55.7543%2C37.6738_55.7514%2C37.6732_55.7485%2C37.6722_55.7455%2C37.6698_55.7427%2C37.6669_55.7403%2C37.6636_55.738%2C37.6605_55.7355%2C37.658_55.7328%2C37.6542_55.7305%2C37.6499_55.7289%2C37.6451_55.7277%2C37.6403_55.7266%2C37.6353_55.7259%2C37.63_55.7254%2C37.6248_55.7251%2C37.6142_55.7259%2C37.6092_55.7267%2C37.6044_55.7278%2C37.5994_55.7289%2C37.5945_55.7298%2C37.59_55.7313%2C37.5862_55.7333%2C37.5817_55.7361%2C37.5785_55.7386%2C37.5749_55.7413%2C37.5723_55.7438%2C37.5701_55.7469%2C37.5682_55.7499%2C37.5665_55.7527%2C37.5654_55.7557&maxprice=55000&minarea=35&minprice=45000&offer_type=flat&polygon_name%5B1%5D=%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C+%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0&room1=1&room2=1&room9=1&sort=price_object_order&totime=7200&type=4"
#AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam-ASgBAgICAUSSA8gQ?cd=1&pmax=55000&pmin=45000&s=104&district=622-645-656-673-696-716-717-738&f=ASgBAQECAkSSA8gQ8AeQUgFAzAg0kFmMWY5ZAUXwCBh7ImZyb20iOjE0MDEwLCJ0byI6bnVsbH0"

CIAN_URL = "https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&foot_min=45&maxprice=45000&metro%5B0%5D=3&metro%5B10%5D=133&metro%5B11%5D=137&metro%5B12%5D=140&metro%5B13%5D=146&metro%5B14%5D=151&metro%5B15%5D=154&metro%5B16%5D=156&metro%5B17%5D=275&metro%5B18%5D=283&metro%5B1%5D=33&metro%5B2%5D=45&metro%5B3%5D=49&metro%5B4%5D=63&metro%5B5%5D=94&metro%5B6%5D=100&metro%5B7%5D=102&metro%5B8%5D=118&metro%5B9%5D=122&minprice=30000&offer_type=flat&only_foot=2&room1=1&room2=1&room9=1&totime=3600&type=4"
AVITO_URL = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&f=ASgBAQICAkSSA8gQ8AeQUgFAzAgkjlmMWQ&metro=2-23-31-39-40-44-68-69-70-76-78-80-85-88-94-104-106-115-121-125-127-135-143-2001-2002-2147-2152-2154-2155-2157-2177&pmax=45000&pmin=30000&proprofile=1&s=104&user=1"


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

        try:
            price = f.find('div', {'data-name': "Price"}).find('div').text
        except: price = ""

        links = f.find_all('a', {'target': '_blank'})
        for a in links:
            if 'https://www.cian.ru/rent/flat/' or 'https://www.cian.ru/sale/flat/' in a['href']:
                if '/cat.php?' not in a['href'] and flat_imgs:
                    flats_items.append({"link": a['href'], "photos": list(set(flat_imgs)), "price": price})
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
