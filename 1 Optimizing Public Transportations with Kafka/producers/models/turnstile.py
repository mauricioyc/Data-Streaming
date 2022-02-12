"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from models.producer import Producer
from models.turnstile_hardware import TurnstileHardware

logger = logging.getLogger(__name__)


class Turnstile(Producer):
    """Produce turnstile events into kafka topic."""

    key_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")

    value_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station):
        """Create the Turnstile"""
        station_name = (
            station.name.lower()
            .replace("/", "_and_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
        )

        super().__init__(
            f"turnstile-info",
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema,
            num_partitions=3,
            num_replicas=1,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)

        logger.info("Producing Turnstile data...")
        for i in range(num_entries):
            self.producer.produce(
                topic=self.topic_name,
                key={"timestamp": self.time_millis()},
                value={
                    'station_id': self.station.station_id,
                    'station_name': self.station.name,
                    'line': self.station.color.name
                },
                value_schema=self.value_schema,
                key_schema=self.key_schema
            )
