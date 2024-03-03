from downloader.downloader import Downloader
from utils.utils import Utils
from db.db import *
import pyfiglet as pyfiglet
import time
import sys
import os
import re
import threading


def download_file(key, url, output_directory):
    downloader = Downloader(output_directory=output_directory)
    download_response = downloader.download_file(url)
    if download_response:
        insert_to_db(key, url, Utils.get_timestamp())

def process_raw_videos(egtea_urls, egtea_dir):
    fname = re.search(r'/([^/]+\.\w+)\?dl=0$', egtea_urls.get('Links to raw videos (28G)')).group(1)
    raw_videos_path = os.path.join(egtea_dir, 'tmp', fname)

    db_result = search_url(egtea_urls.get('Links to raw videos (28G)'))

    if os.path.exists(raw_videos_path) and db_result:
        video_urls = Utils.extract_video_links_from_txt(raw_videos_path)
    else:
        if not os.path.exists(os.path.join(egtea_dir,'tmp')):
            os.mkdir(os.path.join(egtea_dir,'tmp'))
        downloader = Downloader(output_directory=os.path.join(egtea_dir,'tmp'))
        download_response = downloader.download_file(egtea_urls.get('Links to raw videos (28G)'))

        if download_response:
             while not os.path.exists(raw_videos_path):
                 time.sleep(1)
             insert_to_db('video_links.txt', egtea_urls.get('Links to raw videos (28G)'), Utils.get_timestamp())
    return Utils.extract_video_links_from_txt(raw_videos_path)

def main():
    print(Utils.ascii_to_color(pyfiglet.figlet_format("Welcom to Egtea Gaze +",font="slant"),'yellow'))
    init_db()
    egtea_urls = Utils.load_json('../data/egtea_links.json')
    egtea_urls = {list(link.keys())[0]: list(link.values())[0] for link in egtea_urls}

    args = Utils.parse_args()
    egtea_dir = os.path.join(args.out, 'EGTEA')
    Utils.create_directory(egtea_dir)

    download_actions = {
        'readme': ('Readme File', egtea_dir),
        'recipes': ('Recipes', os.path.join(egtea_dir, 'Recipes')),
        'gtea_videos': ('Videos', os.path.join(egtea_dir, 'Videos')),
        'gtea_png': ('Uncompressed PNG Files', os.path.join(egtea_dir, 'Uncompressed_PNG')),
        'trimmed_actions': ('Trimmed Action Clips', os.path.join(egtea_dir, 'Trimmed_Action_Clips')),
        'gaze_data': ('Gaze Data', os.path.join(egtea_dir, 'Gaze_Data')),
        'action_annotations': ('Action Annotations', os.path.join(egtea_dir, 'Action_Annotations')),
        'gtea_labels_71': ('gtea_labels_71', os.path.join(egtea_dir, 'GTEA_Labels_71')),
        'gtea_labels_61': ('gtea_labels_61', os.path.join(egtea_dir, 'GTEA_Labels_61')),
        'hand_masks_2K': ('hand_masks_2K', os.path.join(egtea_dir, 'Hand_Masks_2K')),
        'hand_masks_14K': ('hand_masks_14K', os.path.join(egtea_dir, 'Hand_Masks_14K')),
        'raw_videos': ('Links to raw videos (28G)', os.path.join(egtea_dir, 'tmp'))
    }

    file_download_mapping = {} # dicionary form:{filename: [url, output_directory]}
    if args.all:
        for action, (key, path) in download_actions.items():
            if action != 'raw_videos':
                url = egtea_urls.get(key)
                if url:
                    file_download_mapping[action] = [url, path]
    else:
        for action, (key, path) in download_actions.items():
            if getattr(args, action):
                url = egtea_urls.get(key)
                if url:
                    file_download_mapping[action] = [url, path]

    if args.raw_videos or args.all:
        raw_video_urls = process_raw_videos(egtea_urls, egtea_dir)
        for url in raw_video_urls:
            filename = os.path.splitext(re.search(r'/([^/]+\.\w+)\?dl=0$', url).group(1))[0]
            if filename:
                file_download_mapping[filename] = [url, os.path.join(egtea_dir, 'Raw_Videos')]

    threads = []
    for key, value in file_download_mapping.items():
        if not os.path.exists(value[1]):
            os.mkdir(value[1])
        thread = threading.Thread(target=download_file, args=(key, value[0], value[1]))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
    #TODO: Create docs
    #TODO: In docs add the steps to download the dataset and the tree structure of the dataset