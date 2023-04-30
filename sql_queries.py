import mysql.connector
import datetime


def insert_property(listing, cursor):
    cursor.execute("SELECT estate_id FROM estate_info WHERE title = %s", (listing.data['title'],))

    if (cursor.rowcount == 0):
        if (listing.data['Total Price'] == None):
            return
        insert_property_info(listing, cursor)
        cursor.execute("SELECT estate_id FROM estate_info WHERE title = %s", (listing.data['title'],))
        estate_id = cursor.fetchone()[0]
    else:
        return
    
    insert_property_location(estate_id, listing.data['latitude'], listing.data['longitude'], listing.data['City'], listing.data['Region'], cursor)

    try:
        for media_type in listing.data['Media_types']:
            insert_property_media_type(estate_id, media_type, cursor)
    except:
        pass

    try:
        for security_type in listing.data['Security_types']:
            insert_property_security_type(estate_id, security_type, cursor)
    except:
        pass

    try:
        for extras_type in listing.data['Extras_types']:
            insert_property_extras_type(estate_id, extras_type, cursor)
    except:
        pass

    try:
        for equipment_type in listing.data['Equipment_types']:
            insert_property_equipment_type(estate_id, equipment_type, cursor)
    except:
        pass


def insert_property_info(listing, cursor):
    sql = """
        INSERT INTO estate_info (title, total_price, price_per_square_meter, 
                                area, room_number, build_year, market_type,
                                rent, building_type, floor_no, heating,
                                building_ownership, construction_status,
                                building_material, estate_url, date_added)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = [listing.data['title'], listing.data['Total Price'], listing.data['Price per Square Meter'], \
                listing.data['Area'], listing.data['Room number'], listing.data['Build_year'], \
                listing.data['MarketType'], listing.data['Rent'], listing.data['Building_type'], \
                listing.data['Floor_no'], listing.data['Heating'], listing.data['Building_ownership'], \
                listing.data['Construction_status'], listing.data['Building_material'], 
                listing.url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    
    i = 0
    for value in values:
        if(isinstance(value, list)):
            value = value[0]
            values[i] = value
        i += 1
    
    cursor.execute(sql, values)


def insert_property_location(estate_id, latitude, longitude, City, Region, cursor):
    cursor.execute("SELECT city_id FROM City WHERE city_name = %s", (City,))

    if (cursor.rowcount == 0):
        cursor.execute("INSERT INTO City (city_name) VALUES (%s)", (City,))
        cursor.execute("SELECT city_id FROM City WHERE city_name = %s", (City,))
    
    city_id = cursor.fetchone()[0]

    cursor.execute("SELECT region_id FROM Region WHERE region_name = %s AND city_id = %s", (Region, city_id))

    if (cursor.rowcount == 0):
        cursor.execute("INSERT INTO Region (region_name, city_id) VALUES (%s, %s)", (Region, city_id))
        cursor.execute("SELECT region_id FROM Region WHERE region_name = %s AND city_id = %s", (Region, city_id))
        
    region_id = cursor.fetchone()[0]

    sql = """
        INSERT INTO estate_location (estate_id, latitude, longitude, city_id, region_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (estate_id, latitude, longitude, city_id, region_id)
    cursor.execute(sql, values)


def insert_property_media_type(estate_id, type, cursor):
    cursor.execute("SELECT media_name FROM media_types WHERE media_name = %s", (type,))

    if (cursor.rowcount == 0):
        cursor.execute("INSERT INTO media_types (media_name) VALUES (%s)", (type,))
        cursor.execute("SELECT media_name FROM media_types WHERE media_name = %s", (type,))

    cursor.execute("SELECT media_id FROM media_types WHERE media_name = %s", (type,))
    media_id = cursor.fetchone()[0]

    sql = """
        INSERT INTO estate_media_types (estate_id, media_id)
        VALUES (%s, %s)
    """
    values = (estate_id, media_id)
    cursor.execute(sql, values)


def insert_property_security_type(estate_id, type, cursor):
    cursor.execute("SELECT security_name FROM security_types WHERE security_name = %s", (type,))

    if (cursor.rowcount == 0):
        cursor.execute("INSERT INTO security_types (security_name) VALUES (%s)", (type,))
        cursor.execute("SELECT security_name FROM security_types WHERE security_name = %s", (type,))

    cursor.execute("SELECT security_id FROM security_types WHERE security_name = %s", (type,))
    security_id = cursor.fetchone()[0]

    sql = """
        INSERT INTO estate_security_types (estate_id, security_id)
        VALUES (%s, %s)
    """
    values = (estate_id, security_id)
    cursor.execute(sql, values)


def insert_property_extras_type(estate_id, type, cursor):
    cursor.execute("SELECT extras_name FROM extras_types WHERE extras_name = %s", (type,))

    if (cursor.rowcount == 0):
        cursor.execute("INSERT INTO extras_types (extras_name) VALUES (%s)", (type,))
        cursor.execute("SELECT extras_name FROM extras_types WHERE extras_name = %s", (type,))

    cursor.execute("SELECT extras_id FROM extras_types WHERE extras_name = %s", (type,))
    extras_id = cursor.fetchone()[0]

    sql = """
        INSERT INTO estate_extras_types (estate_id, extras_id)
        VALUES (%s, %s)
    """
    values = (estate_id, extras_id)
    cursor.execute(sql, values)


def insert_property_equipment_type(estate_id, type, cursor):
    cursor.execute("SELECT equipment_name FROM equipment_types WHERE equipment_name = %s", (type,))

    if (cursor.rowcount == 0):
        cursor.execute("INSERT INTO equipment_types (equipment_name) VALUES (%s)", (type,))
        cursor.execute("SELECT equipment_name FROM equipment_types WHERE equipment_name = %s", (type,))

    cursor.execute("SELECT equipment_id FROM equipment_types WHERE equipment_name = %s", (type,))
    equipment_id = cursor.fetchone()[0]

    sql = """
        INSERT INTO estate_equipment_types (estate_id, equipment_id)
        VALUES (%s, %s)
    """
    values = (estate_id, equipment_id)
    cursor.execute(sql, values)


def custom_sql_get(sql, host, user, password):
    db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = 'estate'
    )
    cursor = db.cursor(buffered=True)
    
    cursor.execute(sql)
    return cursor.fetchall()


def get_all_property_info(estate_id, cursor):
    sql = """
        SELECT
            'FLAT' AS 'type of estate',
            e.title,
            c.city_name AS 'City',
            r.region_name AS 'Region',
            e.total_price AS 'Total Price',
            e.price_per_square_meter AS 'Price per Square Meter',
            e.area AS 'Area',
            e.room_number AS 'Room number',
            e.build_year AS 'Build_year',
            e.floor_no AS 'Floor_no',
            e.market_type AS 'MarketType',
            e.rent AS 'Rent',
            e.building_ownership AS 'Building_ownership',
            e.building_type AS 'Building_type',
            e.building_material AS 'Building_material',
            e.estate_url AS 'Estate_url',
            e.date_added AS 'Date_added',
            GROUP_CONCAT(DISTINCT et.extras_name ORDER BY et.extras_name ASC SEPARATOR ',') AS 'Extras_types',
            GROUP_CONCAT(DISTINCT eq.equipment_name ORDER BY eq.equipment_name ASC SEPARATOR ',') AS 'Equipment_types',
            e.construction_status AS 'Construction_status',
            GROUP_CONCAT(DISTINCT em.media_name ORDER BY em.media_name ASC SEPARATOR ',') AS 'Media_types',
            GROUP_CONCAT(DISTINCT es.security_name ORDER BY es.security_name ASC SEPARATOR ',') AS 'Security_types',
            el.latitude,
            el.longitude
        FROM estate_info e
        JOIN estate_location el ON e.estate_id = el.estate_id
        JOIN City c ON el.city_id = c.city_id
        JOIN Region r ON el.region_id = r.region_id
        LEFT JOIN estate_extras_types eet ON e.estate_id = eet.estate_id
        LEFT JOIN extras_types et ON eet.extras_id = et.extras_id
        LEFT JOIN estate_equipment_types eeq ON e.estate_id = eeq.estate_id
        LEFT JOIN equipment_types eq ON eeq.equipment_id = eq.equipment_id
        LEFT JOIN estate_media_types emt ON e.estate_id = emt.estate_id
        LEFT JOIN media_types em ON emt.media_id = em.media_id
        LEFT JOIN estate_security_types est ON e.estate_id = est.estate_id
        LEFT JOIN security_types es ON est.security_id = es.security_id
        GROUP BY e.estate_id
        HAVING e.estate_id = %s;
    """
    cursor.execute(sql, (estate_id,))
    return cursor.fetchone()

def get_unique_values(table, column, cursor):
    cursor.execute("SELECT DISTINCT {} FROM {}".format(column, table))
    return cursor.fetchall()