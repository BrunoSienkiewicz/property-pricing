from bs4 import BeautifulSoup
import sys
import requests
from selenium import webdriver
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
# from scrapingant_client import ScrapingAntClient
import json
from io import StringIO


class MyThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        chrome_options = Options()
        chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        page_content = driver.page_source
        self.soup = BeautifulSoup(page_content, 'lxml')
        driver.quit()

    def get_dict(self):
        script = self.soup.find('script', type='application/json')
        data = json.loads(script.text)
        return data
    

class ListingPage(MyThread):
    def __init__(self, url):
        super().__init__(url)
        self.listing = None

    def get_listing(self):
        dict = self.get_dict()
        self.listing = dict['props']['pageProps']['ad']


class Page(MyThread):
    def __init__(self, url):
        super().__init__(url)
        self.listings = None
    
    def get_listings(self):
        dict = self.get_dict()
        self.listings = dict['props']['pageProps']['data']['searchAds']['items']


def format_listings_to_list(scraped_listings):
    listings = []
    titles = list(scraped_listings.keys())
    for title in titles:
        lst = []
        data = scraped_listings[title]
        lst.append(title)
        data_keys = list(data.keys())
        for key in data_keys:
            lst.append(data[key])
        listings.append(lst)
    return listings


def get_features(scraped_listings):
    features = ['title']
    values = list(scraped_listings.values())
    values = list(values[0].keys())
    for i in values:
        features.append(i)
    return features


# def format_to_cvs(listings):
#     StringData = ""
#     for i in features:
#         if i == features[-1]:
#             StringData += str(i)+"\n"
#             break
#         StringData += str(i)+";"
#     for listing in listings:
#         for data in listing:
#             if data == listing[-1]:
#                 StringData += str(data)+"\n"
#                 break
#             StringData += str(data)+";"
#     to_remove = ['[', ']', "'"]
#     for r in to_remove:
#         StringData = StringData.replace(r,'')
#     return StringData


def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def scrape_page_selenium(url):
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(4)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'lxml')
    return soup


# def scrape_page_scrapingant(url):
#     client = ScrapingAntClient(token='e33452d7fb564f46bdf2a518b22ed206')
#     page_content = client.general_request(url).content
#     soup = BeautifulSoup(page_content, "html.parser")
#     return soup


def scrape_listing_pages(url, pages):
    all_listings = []
    for page in range(1, pages+1):
        page_url = url + f"?page={page}"
        soup = scrape_page_selenium(page_url)
        dict = get_dict(soup)
        listings = dict['props']['pageProps']['data']['searchAds']['items']
        all_listings.append(listings)
        pass
    return all_listings


def get_dict(soup):
    dict = json.loads(soup.find('script', src=None).contents[0])
    return dict


# def update_listings(listings):
#     new_listings = scraped_listings
#     for element in listings:
#         for p in element:
#             title = p['title']
#             if p['totalPrice'] != None:
#                 if title in new_listings:
#                     continue
#                 data = get_data(p)
#                 if data == None:
#                     continue
#                 new_listings[title] = data
#                 pass
#     return new_listings


def get_data(property):
    data ={}
    data['type of estate'] = property['estate']
    location = property['locationLabel']['value']
    location = location.split(', ')
    data['City'] = location[0]
    data['Region'] = location[1]
    data['Total Price'] = property['totalPrice']['value']
    data['Price per Square Meter'] = property['pricePerSquareMeter']['value']
    data['Area'] = property['areaInSquareMeters']
    data['Room number'] = property['roomsNumber']
    data['link'] = property['slug']
    specific_data = get_specific_data(property)
    specific_features = ['Build_year', 'Floor_no', 'Heating', 'MarketType', 
    'Building_ownership', 'Extras_types', 'Rent', 'Equipment_types',
    'Construction_status', 'Building_type', 
    'Building_material', 'Media_types', 'Security_types',
    'latitude', 'longitude']
    if specific_data == None:
        for feature in specific_features:
            data[feature] = 'No Data'
        return data
    for feature in specific_features:
        try:
            if feature == 'latitude' or feature == 'longitude':
                data[feature] = specific_data['location']['coordinates'][feature]
            else:
                data[feature] = specific_data['target'][feature]
        except:
            data[feature] = 'No data'
    return data


def get_specific_data(property):
    url = f'https://www.otodom.pl/pl/oferta/{property["slug"]}'
    soup = scrape_page_selenium(url)
    scripts = soup.find_all('script', src=None)
    listing = json.loads(scripts[-1].contents[0])
    try:
        property_details = listing['props']['pageProps']['ad']
        return property_details
    except:
        return None
    pass



def empty_listings():
    new_listings = {"0": {"0": "0"}}
    return new_listings


def main(args):
    with open('listings.txt', 'r') as file:
        data = file.read().rstrip()
    scraped_listings = json.loads(data)

    if args[3] == 0:
        scraped_listings = empty_listings()

    # miasto = args[1]
    # pages_amt  = args[2] if args[2] != -1 else max_pages
    # data_url = f"https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{miasto}"
    # enable_scraping = args[3]

    # if enable_scraping:
    #     data_dict = get_dict(scrape_page(data_url))
    #     max_pages = data_dict['props']['pageProps']['data']['searchAds']['pagination']['totalPages']
    #     new_scraped_listings = scrape_listing_pages(data_url, pages_amt)
    #     scraped_listings = update_listings(new_scraped_listings)
    #     with open('listings.txt', 'w') as file:
    #         file.write(json.dumps(scraped_listings))

    # features = get_features(scraped_listings)
    # listings = format_listings_to_list(scraped_listings)
    # csv_data = format_to_cvs(listings)

    # with open('listing_data.csv', 'w', encoding="utf-8") as file:
    #     file.write(csv_data)


if __name__ == "__main__":
    main(sys.argv)
