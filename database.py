import csv
import json
from scrape_data import Page, ListingPage


class Database:
    def __init__(self, filename, features, city, pages_amt=1, threads_amt=1):
        self.city = city
        self.data_url = f"https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{city}"
        self.filename = filename
        self.features = features
        self.pages_amt = pages_amt
        self.threads_amt = threads_amt
        self.raw_listings = []

    def scrape_listings(self):
        page_urls = []
        for i in range (self.pages_amt):
            page_urls.append(self.data_url + f'?page={i+1}')

        page_threads = []
        for url in page_urls:
            page_threads.append(Page(url))

        for thread in page_threads:
            thread.start()
        
        for thread in page_threads:
            thread.join()

        listings = []
        for thread in page_threads:
            thread.get_listings()
            listings += thread.listings
        self.raw_listings = listings

    def format_listings(self):
        self.listings = []
        for listing in self.raw_listings:
            self.listings.append(Listing(self.features, listing['slug'], listing))
            if (len(self.listings) == 5):
                break

        for listing in self.listings:
            listing.thread.start()

        for listing in self.listings:
            listing.thread.join()

        for listing in self.listings:
            listing.thread.get_listing()
            listing.get_data()


    def save_to_csv(self):
        with open(self.filename + "csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.features)
            for listing in self.listings:
                writer.writerow(listing)

    def read_csv(self):
        with open(self.filename + ".csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

    def read_json(self):
        with open(self.filename + ".json", 'r') as file:
            data = file.read()
        return json.loads(data)
    
    def save_to_json(self):
        with open(self.filename + ".json", 'w') as file:
            file.write(json.dumps(self._scraped_listings_json))


class Listing:
    def __init__(self, features, slug, listing_dict):
        self.slug = slug
        self.features = features
        self.listing_dict = listing_dict
        self.url = f'https://www.otodom.pl/pl/oferta/{slug}'
        self.thread = ListingPage(self.url)

    def get_data(self):
        data = {}
        data['type of estate'] = self.listing_dict['estate']
        location = self.listing_dict['locationLabel']['value']
        location = location.split(', ')
        data['City'] = self.listing_dict['location']['address']['city']['name']
        data['Region'] = location[1]
        data['Total Price'] = self.listing_dict['totalPrice']['value']
        data['Price per Square Meter'] = self.listing_dict['pricePerSquareMeter']['value']
        data['Area'] = self.listing_dict['areaInSquareMeters']
        data['Room number'] = self.listing_dict['roomsNumber']
        for feature in self.features:
            try:
                if feature == 'latitude' or feature == 'longitude':
                    data[feature] = self.thread.listing['location']['coordinates'][feature]
                else:
                    data[feature] = self.thread.listing['target'][feature]
            except:
                data[feature] = 'No data'
        self.data = data
