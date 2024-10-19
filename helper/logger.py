import logging


class Logger:
    def __init__(self):
        # Create a logger
        self.logger = logging.getLogger(__name__)

        # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        self.logger.setLevel(logging.DEBUG)

        # Create a handler for output (e.g., console)
        self.handler = logging.StreamHandler()

        # Add the handler to the logger
        self.logger.addHandler(self.handler)

    def get_logger(self):
        return self.logger
        