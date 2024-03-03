EGTEA Gaze + Unofficial Downloader
![Egtea Gaze +](/assets/images/dataset_img.png)
==================================

## How to download

1. Clone the repository

   ```bash
   git clone git@github.com:amitsou/EGTEA_Gaze_Plus_Downloader.git
   ```
2. Enter the directory

   ```bash
   cd EGTEA_Gaze_Plus_Downloader
   ```
3. Create the virtual environment and activate it

   ```bash
   python3 -m venv vevn
   source venv/bin/activate
   ```
4. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```
5. Execute the spider to download the appropriate urls from the official web page: [https://cbs.ic.gatech.edu/fpv/](https://cbs.ic.gatech.edu/fpv/)

   ```bash
   cd src/srapper
   scrapy crawl egtea_spider
   ```
   After executing this command a json file will be created in

   ```
   /Egtea_Gaze_Plus_Downloader/data/egtea_links.json
   ```
6. Then, to download the data execute the following:

   ```bash
   cd src/
   python scrapper.py [options] --out <output_directory>
   ```
   The script can be executed using the following arguments:

   ```bash
   --readme: Download the Readme file.
   --recipes: Download the Recipes.
   --raw_videos: Download Raw Videos.
   --gtea_videos: Download GTEA Videos.
   --gtea_png: Download Uncompressed PNG.
   --hand_masks_2K: Download Hand Masks GTEA.
   --hand_masks_14K: Download Hand Masks EGTEA+.
   --trimmed_actions: Download Trimmed Actions.
   --gaze_data: Download Gaze Data.
   --action_annotations: Download Action Annotations.
   --gtea_labels_71: Download GTEA Action Labels.
   --gtea_labels_61: Download EGTEA Action Labels.
   --all: Get all the data.
   ```
7. The final tree structure (assuming you have downloaded the whole dataset) should be the following:

   ```
   EGTEA/
    ├── Action_Annotations/
    │   └── action_annotation.zip
    ├── Gaze_Data/
    │   └── gaze_data.zip
    ├── Gtea_Labels_61/
    │   └── gtea_labels_61.zip
    ├── Gtea_Labels_71/
    │   └── gtea_labels_71.zip
    ├── Hand_Masks_14K/
    │   └── hand14k.zip
    ├── Hand_Masks_2K/
    │   └── hand2K_dataset.zip
    ├── Raw_Videos/
    │   ├── video1.mp4
    │   ├── video2.mp4
    │   └── ...
    ├── Recipes/
    │   └── Recipes.pdf
    ├── Trimmed_Action_Clips/
    │   └── video_clips.tar
    ├── Uncompressed_PNG/
    │   └── gtea_png.zip
    ├── Videos/
    │   └── gtea_videos.zip
    ├── readme.md
    └── tmp/
        └── video_links.txt
   ```
8. Citing
    ```
    @inproceedings{li2018eye,
        title={In the eye of beholder: Joint learning of gaze and actions in first person video},
        author={Li, Yin and Liu, Miao and Rehg, James M},
        booktitle={Proceedings of the European conference on computer vision (ECCV)},
        pages={619--635},
        year={2018}
    }
    ```