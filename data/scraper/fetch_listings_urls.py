import argparse
from helpers.driver_thread import Page
from settings import Settings


class FetchListingsUrls:
    def __init__(self, url):
        self.url = url
        self.page = Page(self.url)

    def start(self):
        self.page.start()
        self.page.join()

    def get_urls(self):
        urls = []
        for listing in self.page.get_listings():
            urls.append(listing['url'])
        return urls

def main(args):
    url = Settings().get('url')
    pages_to_fetch = args.pages_to_fetch

    urls = []
    for i in range(1, pages_to_fetch + 1):
        fetch_listings_urls = FetchListingsUrls(url + f'&page={i}')
        fetch_listings_urls.start()
        urls = urls + fetch_listings_urls.get_urls()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pages_to_fetch', type=int, help='Number of pages to fetch')
    args = parser.parse_args()
    main(args)
