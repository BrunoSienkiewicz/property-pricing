from database import Database


def main():
    features = ['Build_year', 'Floor_no', 'Heating', 'MarketType', 
    'Building_ownership', 'Extras_types', 'Rent', 'Equipment_types',
    'Construction_status', 'Building_type', 
    'Building_material', 'Media_types', 'Security_types',
    'latitude', 'longitude']
    database = Database("test", features, "warszawa", 1, 2)
    database.scrape_listings()
    database.format_listings()
    pass

if __name__ == "__main__":
    main()