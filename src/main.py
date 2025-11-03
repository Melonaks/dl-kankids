import sys
from os import mkdir
from pathlib import Path
import re

from get_episodes_list import get_episodes_list
from get_episode_ims import get_episode_manifest_url
from downloader import download



# 1. Prepare download folder
def prepare_folder(season_url, download_path):
    match = re.search(r'/([^/?#]+)/?(?:[?#].*)?$', season_url)
    folder = f"{match.group(1)}"
    download_folder = download_path.joinpath(folder)
    try:
        mkdir(download_folder)
        print(f"Directory '{download_folder}' created.")
    except FileExistsError:
        print(f"Directory '{download_folder}' already exist (or write permission is not granted)")

    return download_folder


# 2. Parse pages and collect URLs before download
def get_episodes_manifests(season_url):
    print("Scanning for episodes...")
    episodes = get_episodes_list(season_url)
    print(f"{len(episodes)} episodes found!")

    # Obtaining manifest URL and updating each episode accordingly
    print("Parsing manifests (it may take a while)")
    return get_episode_manifest_url(episodes)


# 3. Download!
def download_manager(episodes, target_folder):
    print(f"{len(episodes)} episodes found! Downloading...")
    for e in episodes:
        download(e, target_folder)


def validate_input_args():
    if len(sys.argv) >= 3:  # script name + 2 arguments
        return
    else:
        sys.exit("1 or more arguments are missing!\nEnter URL of a series and download folder\nExample:\n'python main.py \"https://www.kankids.org.il/content/kids/hinuchit-main/its_me/\" \"E:\\series\\\"")


# Obtain launch arguments
if __name__ == "__main__":

    validate_input_args()

    # season_url = sys.argv[1]
    # download_path = Path(sys.argv[2])
    season_url = "https://www.kankids.org.il/content/kids/hinuchit-main/its_me/"
    download_path = Path("D:\downloads")


    download_folder = prepare_folder(season_url, download_path)
    episodes = get_episodes_manifests(season_url)
    download_manager(episodes, download_folder)
    print("Done!")