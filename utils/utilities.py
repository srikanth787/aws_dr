import os
import json

class Utilities:
    """
    Utility class containing static methods for various utility functions.
    """
    @staticmethod
    def read_tags_from_file(filepath):
        """
        Reads the tag values from the given file.

        :param filepath: The path to the file containing the tag values.
        :return: A list of tag values.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found.")

        with open(filepath, 'r') as file:
            tags = json.load(file)

        return tags

    # Additional utility static methods can be added below.


# Usage Example
if __name__ == "__main__":
    tag_filepath = "path_to_tags_file.json"
    tags = Utilities.read_tags_from_file(tag_filepath)
    print(tags)
