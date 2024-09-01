SELECT
  property_id,
  ingestion_timestamp as event_timestamp
FROM property_store.property_info
WHERE date_added BETWEEN '{start_date}' AND '{end_date}'
