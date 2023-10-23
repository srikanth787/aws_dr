# utils/logger.py

import logging
import os
import sys


class CustomLogger:
    def __init__(self, name, log_file="logs/main.log"):
        """
        Initialize a logger that logs to both the console and a file.

        Parameters:
        - name (str): The name of the logger, typically __name__.
        - log_file (str, optional): The path to the log file. Defaults to "logs/main.log".
        """

        # Ensure the directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

        # File handler for logging to a file
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(formatter)

        # Console handler for logging to stdout
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Returns the configured logger object.

        Returns:
        logging.Logger: The configured logger object.
        """
        return self.logger
