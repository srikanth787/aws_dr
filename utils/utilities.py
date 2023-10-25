import json
import os


class Utility:

    @staticmethod
    def read_tags_from_file(file_path):
        """
        Reads a JSON file containing tags and returns a list of tag dictionaries.

        :param file_path: Path to the JSON file containing tags.
        :return: List of tag dictionaries.
        """
        if not os.path.exists(file_path):
            raise ValueError(f"The provided file path {file_path} does not exist.")

        with open(file_path, 'r') as file:
            tags = json.load(file)

        if not isinstance(tags, list):
            raise ValueError("The provided JSON file does not contain a list of tags.")

        return tags

    @staticmethod
    def generate_output_path(account, region, az, date):
        """
        Generates an output path based on provided parameters.

        :param account: AWS account.
        :param region: AWS region.
        :param az: AWS availability zone.
        :param date: Current date in 'YYYY-MM-DD' format.
        :return: Output path string.
        """
        return os.path.join("outputs", account, region, az, date)

    @staticmethod
    def check_file_directory(file_path):
        """
        Checks if the directory for the given file path exists, if not, creates it.

        :param file_path: Path to the file.
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
