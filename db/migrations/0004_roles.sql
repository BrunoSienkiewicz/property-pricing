-- Create admin role
CREATE ROLE admin;
GRANT ALL ON SCHEMA public TO admin;
GRANT ALL ON SCHEMA property_store TO admin;
GRANT ALL ON SCHEMA feature_store TO admin;

-- Create feature store role
CREATE ROLE feature_store;
GRANT ALL PRIVILEGES ON SCHEMA feature_store TO feature_store;
GRANT SELECT ON ALL TABLES IN SCHEMA property_store TO feature_store;


