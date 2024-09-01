CREATE SCHEMA IF NOT EXISTS property_store;
CREATE SCHEMA IF NOT EXISTS feature_store;

-- Create property_info table
CREATE TABLE property_store.property_info(
  property_id SERIAL NOT NULL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  property_url VARCHAR(255) NOT NULL UNIQUE,

  -- location
  city VARCHAR(32) NOT NULL,
  region VARCHAR(32) NOT NULL,
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,

  -- property details
  total_price INT NOT NULL,
  price_per_square_meter INT NOT NULL,
  area INT NOT NULL,
  market_type VARCHAR(255),

  -- property features
  floor INT,
  year_built INT,
  rooms INT,

  date_added DATE NOT NULL,
  ingestion_timestamp TIMESTAMP
);

-- Create property_extras table
CREATE TABLE property_store.property_extras(
  property_id INT NOT NULL,
  extras_name VARCHAR(64) NOT NULL,
  FOREIGN KEY (property_id) REFERENCES property_store.property_info(property_id)
);

-- Create property_media table
CREATE TABLE property_store.property_media(
  property_id INT NOT NULL,
  media_name VARCHAR(64) NOT NULL,
  FOREIGN KEY (property_id) REFERENCES property_store.property_info(property_id)
);

-- Create property_security table
CREATE TABLE property_store.property_security(
  property_id INT NOT NULL,
  security_name VARCHAR(64) NOT NULL,
  FOREIGN KEY (property_id) REFERENCES property_store.property_info(property_id)
);

-- Create property_equipment table
CREATE TABLE property_store.property_equipment(
  property_id INT NOT NULL,
  equipment_name VARCHAR(64) NOT NULL,
  FOREIGN KEY (property_id) REFERENCES property_store.property_info(property_id)
);
