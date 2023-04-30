DROP TABLE IF EXISTS estate_location CASCADE;
DROP TABLE IF EXISTS estate_extras_types CASCADE;
DROP TABLE IF EXISTS estate_media_types CASCADE;
DROP TABLE IF EXISTS estate_security_types CASCADE;
DROP TABLE IF EXISTS estate_equipment_types CASCADE;
DROP TABLE IF EXISTS Region CASCADE;
DROP TABLE IF EXISTS estate_info CASCADE;
DROP TABLE IF EXISTS City CASCADE;
DROP TABLE IF EXISTS extras_types CASCADE;
DROP TABLE IF EXISTS media_types CASCADE;
DROP TABLE IF EXISTS security_types CASCADE;
DROP TABLE IF EXISTS equipment_types CASCADE;

-- Create estate_info table
CREATE TABLE estate_info(
  estate_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL UNIQUE,
  total_price INT NOT NULL,
  price_per_square_meter INT NOT NULL,
  area INT NOT NULL,
  room_number INT NOT NULL,
  build_year INT,
  market_type VARCHAR(255),
  rent INT,
  building_type VARCHAR(255),
  floor_no INT,
  heating VARCHAR(255),
  building_ownership VARCHAR(255),
  construction_status VARCHAR(255),
  building_material VARCHAR(255),
  estate_url VARCHAR(255),
  date_added DATE NOT NULL
);

-- Create City table
CREATE TABLE City(
  city_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  city_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create Region table
CREATE TABLE Region(
  region_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  region_name VARCHAR(255) NOT NULL UNIQUE,
  city_id INT NOT NULL,
  FOREIGN KEY (city_id) REFERENCES City(city_id)
);

-- Create extras_types table
CREATE TABLE extras_types(
  extras_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  extras_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create media_types table
CREATE TABLE media_types(
  media_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  media_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create security_types table
CREATE TABLE security_types(
  security_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  security_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create equipment_types table
CREATE TABLE equipment_types(
  equipment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  equipment_name VARCHAR(255) NOT NULL UNIQUE
);

-- Create estate_location table
CREATE TABLE estate_location(
  estate_id INT NOT NULL,
  latitude FLOAT(10,6),
  longitude FLOAT(10,6),
  city_id INT NOT NULL,
  region_id INT NOT NULL,
  PRIMARY KEY (estate_id),
  FOREIGN KEY (estate_id) REFERENCES estate_info(estate_id),
  FOREIGN KEY (city_id) REFERENCES City(city_id),
  FOREIGN KEY (region_id) REFERENCES Region(region_id)
);

-- Create estate_extras_types table
CREATE TABLE estate_extras_types(
  estate_id INT NOT NULL,
  extras_id INT NOT NULL,
  PRIMARY KEY (estate_id, extras_id),
  FOREIGN KEY (estate_id) REFERENCES estate_info(estate_id),
  FOREIGN KEY (extras_id) REFERENCES extras_types(extras_id)
);

-- Create estate_media_types table
CREATE TABLE estate_media_types(
  estate_id INT NOT NULL,
  media_id INT NOT NULL,
  PRIMARY KEY (estate_id, media_id),
  FOREIGN KEY (estate_id) REFERENCES estate_info(estate_id),
  FOREIGN KEY (media_id) REFERENCES media_types(media_id)
);

-- Create estate_security_types table
CREATE TABLE estate_security_types(
  estate_id INT NOT NULL,
  security_id INT NOT NULL,
  PRIMARY KEY (estate_id, security_id),
  FOREIGN KEY (estate_id) REFERENCES estate_info(estate_id),
  FOREIGN KEY (security_id) REFERENCES security_types(security_id)
);

-- Create estate_equipment_types table
CREATE TABLE estate_equipment_types(
  estate_id INT NOT NULL,
  equipment_id INT NOT NULL,
  PRIMARY KEY (estate_id, equipment_id),
  FOREIGN KEY (estate_id) REFERENCES estate_info(estate_id),
  FOREIGN KEY (equipment_id) REFERENCES equipment_types(equipment_id)
);
