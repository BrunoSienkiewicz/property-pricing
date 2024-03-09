from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
from selenium.webdriver.chrome.options import Options
import json


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
