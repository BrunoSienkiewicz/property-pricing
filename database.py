import csv
import json
from scrape_data import Page, ListingPage
from sql_queries import insert_property, get_all_property_info
import mysql.connector
from word2number import w2n


class Database:
    def __init__(self, host, user, password, filename, city, pages_amt=1, threads_amt=1):
        self.city = city
        self.data_url = f"https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/{city}"
        self.filename = filename
        self.specific_features = ['Build_year', 'Floor_no', 'Heating', 'MarketType', 
        'Building_ownership', 'Extras_types', 'Rent', 'Equipment_types',
        'Construction_status', 'Building_type', 
        'Building_material', 'Media_types', 'Security_types',
        'latitude', 'longitude']
        self.host = host
        self.user = user
        self.password = password
        self.pages_amt = pages_amt
        self.threads_amt = threads_amt
        self.raw_listings = []

    def scrape_listings(self):
        page_urls = []
        for i in range (self.pages_amt):
            page_urls.append(self.data_url + f'?page={i+1}')

        page_threads = []
        idx = 0
        remaining = len(page_urls) % self.threads_amt
        for url in page_urls:
            page_threads.append(Page(url))
            page_threads[idx].start()
            if (len(page_threads) % self.threads_amt == 0 and idx>0):
                for thread in page_threads[idx-self.threads_amt:idx]:
                    thread.join()
                
                for thread in page_threads[idx-self.threads_amt:idx]:
                    thread.get_listings()
                    self.raw_listings += thread.listings
            idx += 1

        for thread in page_threads[idx-remaining:idx]:
            thread.join()

        for thread in page_threads[idx-remaining:idx]:
            thread.get_listings()
            self.raw_listings += thread.listings

    def format_listings(self):
        self.listings = []
        idx = 0
        remaining = len(self.raw_listings) % self.threads_amt
        for listing in self.raw_listings:
            self.listings.append(Listing(self.specific_features, listing['slug'], listing))
            self.listings[idx].thread.start()
            if (len(self.listings) % self.threads_amt == 0 and idx>0):
                for listing in self.listings[idx-self.threads_amt:idx]:
                    listing.thread.join()
                
                for listing in self.listings[idx-self.threads_amt:idx]:
                    listing.thread.get_listing()
                    listing.get_data()
            idx += 1

        for listing in self.listings[idx-remaining:idx]:
            listing.thread.join()

        for listing in self.listings:
            listing.thread.get_listing()
            listing.get_data()

        self.features = self.listings[0].data.keys()

    def insert_to_db(self):
        db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = 'estate'
        )
        cursor = db.cursor(buffered=True)

        for listing in self.listings:
            insert_property(listing, cursor)

        db.commit()
        db.close()

    def get_property_from_db(self, estate_id):
        db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = 'estate'
        )
        cursor = db.cursor(buffered=True)

        result = get_all_property_info(estate_id, cursor)
        db.close()
        return result

    def save_to_csv(self):
        with open(self.filename + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.features)
            for listing in self.listings:
                writer.writerow(list(listing.data.values()))
    
    def save_to_json(self):
        with open(self.filename + ".json", 'w') as file:
            lst = []
            for listing in self.listings:
                lst.append(listing.data)
            json.dump(lst, file, indent=4)


class Listing:
    def __init__(self, specific_features, slug, listing_dict):
        self.slug = slug
        self.specific_features = specific_features
        self.listing_dict = listing_dict
        self.url = f'https://www.otodom.pl/pl/oferta/{slug}'
        self.thread = ListingPage(self.url)

    def get_data(self):
        data = {}
        data['type of estate'] = self.listing_dict['estate']
        data['title'] = self.listing_dict['title']
        location = self.listing_dict['locationLabel']['value']
        location = location.split(', ')
        data['City'] = self.listing_dict['location']['address']['city']['name']
        data['Region'] = location[1]
        try:
            data['Total Price'] = self.listing_dict['totalPrice']['value']
        except:
            data['Total Price'] = None
        try:
            data['Price per Square Meter'] = self.listing_dict['pricePerSquareMeter']['value']
        except:
            data['Price per Square Meter'] = None
        data['Area'] = self.listing_dict['areaInSquareMeters']
        data['Room number'] = w2n.word_to_num(self.listing_dict['roomsNumber'].lower())
        for feature in self.specific_features:
            try:
                if feature == 'latitude' or feature == 'longitude':
                    data[feature] = self.thread.listing['location']['coordinates'][feature]
                else:
                    data[feature] = self.thread.listing['target'][feature]
            except:
                data[feature] = None

        if data['Floor_no'] is not None:
            if data['Floor_no'][0] == 'ground_floor':
                data['Floor_no'] = 0
            else:
                data['Floor_no'] = int(data['Floor_no'][0][-1])
        
        self.data = data
