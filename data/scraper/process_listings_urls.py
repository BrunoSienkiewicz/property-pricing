import argparse
from settings import Settings
from helpers.driver_thread import ListingPage


class ProcessListing:
    def __init__(self, url):
        self.url = url

    def start(self):
        self.listing_page = ListingPage(self.url)
        self.listing_page.start()
        self.listing_page.join()

    def get_listing(self):
        return self.listing_page.get_listing()


def main(args):
    listing_url = Settings().LISTING_URL + args.url

