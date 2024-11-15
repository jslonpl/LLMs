import os
import sys
import logging

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from src.network.downloader import Downloader

def main():
    filename = 'cenzura.txt'
    downloader = Downloader(filename)

    print(downloader.get_file_txt())




if __name__ == "__main__":
    main()