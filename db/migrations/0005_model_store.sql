CREATE SCHEMA model_store;

CREATE TABLE model_store.model (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_description TEXT,
    model_version VARCHAR(255) NOT NULL,
    model_binary BYTEA NOT NULL,
    model_metadata JSONB NOT NULL,
    model_ordinal_encoder BYTEA,
    model_ohe_encoder BYTEA,
    model_scaler BYTEA,
    model_creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    model_last_update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (model_name, model_version)
);

CREATE INDEX model_store_model_name_version_idx ON model_store.model (model_name, model_version);

