-- Index: date added
CREATE INDEX idx_date_added ON property_store.property_info(date_added);

-- Index: property_id_property_info
CREATE INDEX idx_property_id_property_info ON property_store.property_info(property_id);

-- Index: ingestion_timestamp
CREATE INDEX idx_ingestion_timestamp ON property_store.property_info(ingestion_timestamp);

-- Index: property_id_property_extras
CREATE INDEX idx_property_id_property_extras ON property_store.property_extras(property_id);

-- Index: property_id_property_media
CREATE INDEX idx_property_id_property_media ON property_store.property_media(property_id);

-- Index: property_id_property_security
CREATE INDEX idx_property_id_property_security ON property_store.property_security(property_id);

-- Index: property_id_property_equipment
CREATE INDEX idx_property_id_property_equipment ON property_store.property_equipment(property_id);

