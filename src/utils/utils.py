from datetime import datetime
import os
import json
import argparse

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def ascii_to_color(string, color) -> str:
        """
        Converts the given string to colored ASCII text.

        Args:
            string (str): The string to be converted.
            color (str): The color to be applied to the string.
                         Available colors: 'blue', 'yellow', 'green', 'red'.

        Returns:
            str: The colored ASCII text.

        """
        color_code = {'blue': '\033[34m',
                      'yellow': '\033[33m',
                      'green': '\033[32m',
                      'red': '\033[31m'
                      }
        return color_code[color] + str(string) + '\033[0m'

    @staticmethod
    def get_timestamp() -> str:
        """
        Get the current time as a formatted string.

        Returns:
            str: The current time in the format "%Y-%m-%d %H:%M:%S".
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create_directory(directory: str) -> None:
        """
        Creates a directory if it doesn't already exist.

        Args:
            directory (str): The path of the directory to be created.

        Returns:
            None
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def rename_json_keys(json_data: list) -> list:
        """
        Renames specific keys in a list of JSON objects.

        Args:
            json_data (list): A list of JSON objects.

        Returns:
            list: The modified list of JSON objects with renamed keys.
            """
        key_map = {
            "Action Labels (new)": "gtea_labels_71",
            "Action Labels (old)": "gtea_labels_61",
        }

        for item in json_data:
            if "Hand Masks" in item:
                url = item["Hand Masks"]
                if "hand2K_dataset" in url:
                    item["hand_masks_2K"] = url
                    del item["Hand Masks"]
                elif "hand14k" in url:
                    item["hand_masks_14K"] = url
                    del item["Hand Masks"]

        for item in json_data:
            for old_key, new_key in key_map.items():
                if old_key in item:
                    item[new_key] = item.pop(old_key)

        return json_data

    @staticmethod
    def load_json(file_path: str) -> dict:
        """
        Load JSON data from a file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The loaded JSON data.

        Raises:
            Exception: If the file is not found.
            """
        try:
            with open(file_path) as f:
                data = json.load(f)
                data = Utils.rename_json_keys(data)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except Exception as e:
            raise Exception(f"Error loading JSON from file: {e}") from e
        return data

    @staticmethod
    def extract_video_links_from_txt(file_path: str) -> list:
        """
        Extracts video links from a text file.

        Args:
            file_path (str): The path to the text file.

        Returns:
            list: A list of video links extracted from the text file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.readlines()
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """
        Parse command line arguments.

        Returns:
            argparse.Namespace: Parsed command line arguments.
        """
        parser = argparse.ArgumentParser(description='Scrapper for EGTEA')
        parser.add_argument('--readme', action='store_true', default=False, help='Download the Readme file')
        parser.add_argument('--recipes', action='store_true', default=False, help='Download the Recipes')
        parser.add_argument('--raw_videos', action='store_true', default=False, help='Download Raw Videos')
        parser.add_argument('--gtea_videos', action='store_true', default=False, help='Download GTEA Videos')
        parser.add_argument('--gtea_png', action='store_true', default=False, help='Download Uncompressed PNG')
        parser.add_argument('--hand_masks_2K', action='store_true', default=False, help='Download Hand Masks GTEA')
        parser.add_argument('--hand_masks_14K', action='store_true', default=False, help='Download Hand Masks EGTEA+')
        parser.add_argument('--trimmed_actions', action='store_true', default=False, help='Download Trimmed Actions')
        parser.add_argument('--gaze_data', action='store_true', default=False, help='Download Gaze Data')
        parser.add_argument('--action_annotations', action='store_true', default=False, help='Download Action Annotations')
        parser.add_argument('--gtea_labels_71', action='store_true', default=False, help='Download GTEA Action Labels')
        parser.add_argument('--gtea_labels_61', action='store_true', default=False, help='Download EGTEA Action Labels')
        parser.add_argument('--all', action='store_true', default=False, help='Get all the data')
        parser.add_argument('--out', default='../data', help='Output directory to save the data')
        return parser.parse_args()