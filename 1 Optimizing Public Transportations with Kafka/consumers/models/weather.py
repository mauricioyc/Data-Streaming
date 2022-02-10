"""Contains functionality related to Weather"""
import json
import logging

logger = logging.getLogger(__name__)


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

    def process_message(self, message):
        """Handles incoming weather data"""
        try:
            value = json.loads(message.value())
            self.temperature = value["temperature"]
            self.status = value["status"]
            logger.debug(value)
        except Exception as error_info:
            logger.error("Error while handling weather message %s", error_info)
