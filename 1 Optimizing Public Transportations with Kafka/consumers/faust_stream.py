"""Defines trends calculations for stations"""
import logging

import faust

logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    """Station to consume in Kafka."""

    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    """TransformedStation to produce in Kafka."""

    station_id: int
    station_name: str
    order: int
    line: str


app = faust.App("stations-stream",
                broker="kafka://localhost:9092", store="memory://")

topic = app.topic(
    "connector_stations",
    key_type=str,
    value_type=Station,
)

out_topic = app.topic("faust_stations_transformed", partitions=1)

table = app.Table(
    'faust_stations_transformed_table',
    default=TransformedStation,
    partitions=1,
    changelog_topic=out_topic,
)


@app.agent(topic)
async def transform_stations(station_events):
    """Transform stations event into table."""

    async for station_event in station_events:
        line = "red" if station_event.red else "blue" if station_event.blue else "green"

        table[station_event.station_id] = TransformedStation(
            station_id=station_event.station_id,
            station_name=station_event.station_name,
            order=station_event.order,
            line=line
        )


if __name__ == "__main__":
    app.main()
