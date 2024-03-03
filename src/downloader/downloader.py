from tqdm import tqdm
import os
import re
import sys
import time
import requests
import logging


class Downloader:
    def __init__(self, output_directory="../../data", max_retries=3, retry_delay=1):
        self.output_directory = output_directory
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)

    def download_file(self, file_url):
        logging.basicConfig(level=logging.INFO)
        download_url = file_url.replace('?dl=0', '?dl=1')

        for _ in range(self.max_retries):
            try:
                response = requests.get(download_url, stream=True)
                if response.status_code == 200:
                    filename = self.extract_filename_from_header(response.headers.get('content-disposition'))
                    if not filename:
                        filename = self.extract_filename_from_url(file_url)
                    file_path = os.path.join(self.output_directory, filename)

                    if os.path.exists(file_path):
                        self.logger.info(f"File '{filename}' already exists. Skipping download.")
                        return True

                    with open(file_path, 'wb') as file:
                        total_size = int(response.headers.get('content-length', 0))
                        with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    file.write(chunk)
                                    pbar.update(len(chunk))
                    self.logger.info(f"Downloaded {filename}")
                    return True
                elif response.status_code == 429:
                    self.logger.warning("Too many requests. Waiting before retrying...")
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error(f"Failed to download file. Status code: {response.status_code}")
                    return False
            except requests.RequestException as e:
                self.logger.error(f"Error occurred during download: {e}")
                return False
        self.logger.error(f"Max retries reached. Failed to download file: {file_url}")
        return False

    def extract_filename_from_header(self, content_disposition):
        if content_disposition:
            match = re.search(r'filename\*?=[\'\"]?(?:UTF-\d+\')?([^;\r\n\"]+)', content_disposition)
            if match:
                return match.group(1).strip('"')
            else:
                return re.search(r'filename=[\'\"]?([^;\r\n\"]+)', content_disposition).group(1).strip('"')
        return None

    def extract_filename_from_url(self, file_url):
        if re.search(r'/([^/]+\.\w+)\?dl=0$', file_url):
            return re.search(r'/([^/]+\.\w+)\?dl=0$', file_url).group(1)
        return None