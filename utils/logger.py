import logging
import os
from datetime import datetime


class CustomLogger:
    def __init__(self, name="aws_dr_scripts"):
        """
        Initialize the CustomLogger class.

        Parameters:
        - name: The name of the logger.
        """
        self.name = name
        self.logger = logging.getLogger(self.name)
        self._setup()

    def _setup(self):
        """
        Setup the logger configurations.
        """
        log_format = "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s"
        self.logger.setLevel(logging.INFO)

        # Define the path to store logs using the current date
        base_path = "logs"
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_path = os.path.join(base_path, current_date)

        # If the path doesn't exist, create the directories
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        # Create and add file handler to logger
        log_file = os.path.join(log_path, f"{self.name}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(file_handler)

        # Also add stream handler to logger (optional, can be removed if not needed)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        """
        Return the logger instance.
        """
        return self.logger


