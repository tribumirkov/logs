"""
Dataset downloader module.

This module handles downloading and extracting the BGL dataset
if it is not already present in the data directory.
"""

import os
import sys
import tarfile
import urllib.request
import urllib.error


def _make_progress_hook():
    """Create a progress hook for urllib downloads."""
    last_percent = -1

    def hook(block_num: int, block_size: int, total_size: int):
        nonlocal last_percent
        if total_size > 0:
            percent = min(100, int(block_num * block_size * 100 / total_size))
            if percent != last_percent:
                last_percent = percent
                length = 40
                filled = int(length * percent / 100)
                progress = "=" * filled + "-" * (length - filled)
                mb_downloaded = (block_num * block_size) / (1024 * 1024)
                mb_total = total_size / (1024 * 1024)
                sys.stdout.write(
                    f"\r  [{progress}] {percent}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)"
                )
                sys.stdout.flush()
                if percent == 100:
                    print()

    return hook


def download_bgl(url: str, data_dir: str = "data"):
    """
    Download and extract the BGL dataset if BGL.log is missing.

    Args:
        url (str): The URL to download the BGL dataset from.
        data_dir (str): The directory to store the dataset in.

    Raises:
        SystemExit: If the download fails after retries.
    """
    log_file = os.path.join(data_dir, "BGL.log")
    if os.path.exists(log_file):
        print(f"Dataset already exists at {log_file}")
        return

    os.makedirs(data_dir, exist_ok=True)
    tar_path = os.path.join(data_dir, "BGL.tar.gz")

    print(f"Downloading BGL dataset from {url}...")
    print("  (This may take a few minutes depending on your connection)")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            urllib.request.urlretrieve(url, tar_path, _make_progress_hook())
            break
        except urllib.error.URLError as e:
            if attempt < max_retries:
                print(f"\n  Download failed (attempt {attempt}/{max_retries}): {e}")
                print("  Retrying...")
            else:
                print(f"\n  Download failed after {max_retries} attempts: {e}")
                print("  Please check your internet connection and try again.")
                sys.exit(1)

    print("Extracting dataset...")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=data_dir, filter="data")

    print(f"Dataset ready at {log_file}")

    if os.path.exists(tar_path):
        os.remove(tar_path)
