from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapper.scrapper.spiders.egtea_spider import EgteaSpiderSpider
import argparse
import json

def setup_crawler() -> None:
    process = CrawlerProcess(get_project_settings())
    process.crawl(EgteaSpiderSpider)
    process.start()


def download_files():
    pass

def load_json() -> dict:
    try:
        with open('../data/results.json') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise Exception(e)
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Scrapper for EGTEA')
    parser.add_argument('-r','--readme', type=str, action='store_true', help='Download the Readme file')
    parser.add_argument('-rec','--recipes', type=str, action='store_true', help='Download the Recipes', Description='Pdf file with the recipes')
    parser.add_argument('-raw','--raw_video', type=str,  action='store_true', help='Download Raw Videos', Description='Txt file with links to the raw videos.')
    parser.add_argument('-v','--video', type=str, action='store_true', help='Download GTEA Videos')
    parser.add_argument('-png','--uncompressed_png', type=str,  action='store_true', help='Download Uncompressed PNG')
    parser.add_argument('-gtea','--hand_masks_gtea', type=str, action='store_true', help='Download Hand Masks GTEA')
    parser.add_argument('-egtea','--hand_masks_egtea', type=str, action='store_true', help='Download Hand Masks EGTEA+')
    parser.add_argument('-taction','--trimmed_actions', type=str, action='store_true', help='Download Trimmed Actions')
    parser.add_argument('-g','--gaze_data', type=str, action='store_true', help='Download Gaze Data')
    parser.add_argument('-aa','--action_annotations', type=str,  action='store_true', help='Download Action Annotations')
    parser.add_argument('-gtea_l','--gtea_labels', type=str, action='store_true', help='Download GTEA Action Labels')
    parser.add_argument('-egtea_l','--egtea_labels', type=str, action='store_true', help='Download EGTEA Action Labels')
    parser.add_argument('-o','--out', type=str, action='store_true', required=True, help='Output directory to save the data')
    parser.add_argument('-a','--all', type=str, action='store_true', help='Get all the data')
    return parser.parse_args()


"""
def main():
    args = parse_args()

    actions = {
        'all': action_all,
        'readme': action_readme,
        'recipes': action_recipes,
        'raw_video': action_raw_video,
        'video': action_video,
        'uncompressed_png': action_uncompressed_png,
        'hand_masks14K': action_hand_masks14K,
        'hand_masks20K': action_hand_masks20K,
        'trimmed_actions': action_trimmed_actions,
        'gaze_data': action_gaze_data,
        'action_annotations': action_action_annotations,
        'labels_old': action_labels_old,
        'labels_new': action_labels_new
    }

    for arg, action in actions.items():
        if getattr(args, arg):
            action(args)


def action_all(args):
    pass

def action_readme(args):
    pass

def action_recipes(args):
    pass

def action_raw_video(args):
    pass

def action_video(args):
    pass

def action_uncompressed_png(args):
    pass

def action_hand_masks14K(args):
    pass

def action_hand_masks20K(args):
    pass

def action_trimmed_actions(args):
    pass

def action_gaze_data(args):
    pass

def action_action_annotations(args):
    pass

def action_labels_old(args):
    pass

def action_labels_new(args):
    pass
"""


def main():
    data = load_json()
    print(json.dumps(data, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
