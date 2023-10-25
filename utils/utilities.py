import os
import json
from datetime import datetime

class Utilities:

    @staticmethod
    def get_current_date():
        """
        Returns the current date in YYYY-MM-DD format.

        Returns:
            str: Current date in YYYY-MM-DD format.
        """
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def read_tags_from_file(file_path):
        """
        Read the tag values from a specified file.

        Parameters:
            file_path (str): Path to the file containing tag values.

        Returns:
            list: List of tags.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as file:
            tags = file.readlines()

        # Strip out any newlines or spaces
        return [tag.strip() for tag in tags]

    @staticmethod
    def save_to_json(data, file_path):
        """
        Save a dictionary to a specified JSON file.

        Parameters:
            data (dict): Data to be saved to file.
            file_path (str): Path to the JSON file.
        """
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_from_json(file_path):
        """
        Load a dictionary from a specified JSON file.

        Parameters:
            file_path (str): Path to the JSON file.

        Returns:
            dict: Data loaded from the JSON file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as file:
            data = json.load(file)

        return data
