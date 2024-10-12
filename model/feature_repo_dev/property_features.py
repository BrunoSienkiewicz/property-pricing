from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, ValueType
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)
from feast.types import Float64, Int64, String, UnixTimestamp

property_id = Entity(
    name="property_id",
    join_keys=["property_id"],
    value_type=ValueType.INT64,
    description="Property ID",
)

property_info_source = PostgreSQLSource(
    name="property_info",
    query="SELECT * FROM property_store.property_info",
    timestamp_field="ingestion_timestamp",
)

property_info_fv = FeatureView(
    name="property_info",
    entities=[property_id],
    ttl=timedelta(days=30),
    schema=[
        Field(name="total_price", dtype=Int64),
        Field(name="area", dtype=Float64),
        Field(name="market_type", dtype=String),
        Field(name="city", dtype=String),
        Field(name="region", dtype=String),
        Field(name="longitude", dtype=Float64),
        Field(name="latitude", dtype=Float64),
        Field(name="floor", dtype=Int64),
        Field(name="year_built", dtype=Int64),
        Field(name="rooms", dtype=Int64),
        Field(name="date_added", dtype=UnixTimestamp),
    ],
    online=True,
    source=property_info_source,
)

property_info_v1 = FeatureService(
    name="property_info_v1",
    features=[property_info_fv],
    tags={"release": "development"},
)
