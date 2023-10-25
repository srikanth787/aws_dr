import logging
import os
from datetime import datetime


class Logger:
    """
    A class that provides logging capabilities.
    """

    def __init__(self, log_dir, module_name):
        """
        Initialize Logger.

        Parameters:
            - log_dir (str): Directory where the logs will be stored.
            - module_name (str): Name of the module requesting the logger.
        """
        self.log_dir = log_dir
        self.module_name = module_name
        self._prepare_log_dir()

    def _prepare_log_dir(self):
        """
        Create log directory if it doesn't exist.
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def get_logger(self):
        """
        Setup and return a logger.

        Returns:
            logging.Logger: Configured logger.
        """
        # Create logger for the provided module
        logger = logging.getLogger(self.module_name)
        logger.setLevel(logging.DEBUG)

        # Define format for logs
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] - %(message)s'
        )

        # Create console handler and set the level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Create file handler for storing logs in a file
        today_date = datetime.now().strftime('%Y-%m-%d')
        log_file_path = os.path.join(self.log_dir, f'{self.module_name}_{today_date}.log')
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger
