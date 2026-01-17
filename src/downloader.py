"""
Dataset downloader module.

This module handles downloading and extracting the BGL dataset
if it is not already present in the data directory.
"""

import os
import tarfile
import urllib.request


def download_bgl(url: str, data_dir: str = "data"):
    """
    Download and extract the BGL dataset if BGL.log is missing.

    Args:
        url (str): The URL to download the BGL dataset from.
        data_dir (str): The directory to store the dataset in.
    """
    log_file = os.path.join(data_dir, "BGL.log")
    if os.path.exists(log_file):
        print(f"Dataset already exists at {log_file}")
        return

    os.makedirs(data_dir, exist_ok=True)
    tar_path = os.path.join(data_dir, "BGL.tar.gz")

    print(f"Downloading BGL dataset from {url}...")
    urllib.request.urlretrieve(url, tar_path)

    print("Extracting dataset...")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=data_dir)

    print(f"Dataset extracted to {data_dir}")

    # Cleanup the tarball
    if os.path.exists(tar_path):
        os.remove(tar_path)
