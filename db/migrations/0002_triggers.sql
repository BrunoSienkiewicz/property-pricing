-- Trigger: on insert add ingested timestamp
CREATE OR REPLACE FUNCTION add_ingestion_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.ingestion_timestamp = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_ingestion_timestamp_trigger
BEFORE INSERT ON property_store.property_info
FOR EACH ROW
EXECUTE FUNCTION add_ingestion_timestamp();

