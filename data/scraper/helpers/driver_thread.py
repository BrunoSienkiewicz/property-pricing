from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
from selenium.webdriver.chrome.options import Options
import json


class DriverThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        self.soup = None

    def run(self):
        chrome_options = Options()
        chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        page_content = driver.page_source
        self.soup = BeautifulSoup(page_content, 'lxml')
        driver.quit()

    def get_dict(self):
        if self.soup is None:
            raise Exception('Page not fetched')

        script = self.soup.find('script', type='application/json')
        data = json.loads(script.text)
        return data

    def finished(self):
        return self.soup is not None
    

class ListingPage(DriverThread):
    def __init__(self, url):
        super().__init__(url)

    def get_listing(self):
        dict = self.get_dict()
        return dict['props']['pageProps']['ad']


class Page(DriverThread):
    def __init__(self, url):
        super().__init__(url)
    
    def get_listings(self):
        dict = self.get_dict()
        return dict['props']['pageProps']['data']['searchAds']['items']
