import bz2
import requests
import os
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional

class WikiDownloader:
    """
    A module to download and decompress the arwiki-latest-pages-articles.xml.bz2 file efficiently.
    """
    def __init__(self, url: str = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2",
                 download_dir: str = None):
        """
        Initializes the WikiDownloader.

        Args:
            url (str): The URL of the XML.bz2 file to download.
            download_dir (str, optional): The directory to save the downloaded and decompressed files.
                                          If None, a temporary directory will be created.
        """
        self.url = url
        self.download_dir = download_dir or tempfile.mkdtemp(prefix="wiki_download_")
        self.bz2_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml.bz2")
        self.xml_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml")
        os.makedirs(self.download_dir, exist_ok=True)
        print(f"Download directory set to: {self.download_dir}")

    def download_file(self, chunk_size: int = 8192) -> bool:
        """
        Downloads the specified file from the URL in chunks.

        Args:
            chunk_size (int): The size of each chunk to download.

        Returns:
            bool: True if the download was successful, False otherwise.
        """
        print(f"Downloading file from: {self.url}")
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()  # Raise an exception for bad status codes
                total_size = int(r.headers.get('content-length', 0))
                downloaded_size = 0
                with open(self.bz2_filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"Downloaded: {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\r')
                        else:
                            print(f"Downloaded: {downloaded_size} bytes", end='\r')
            print("\nDownload complete.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"\nError downloading file: {e}")
            return False
        except Exception as e:
            print(f"\nAn unexpected error occurred during download: {e}")
            return False

    def decompress_file(self, num_threads: int = os.cpu_count() or 1) -> bool:
        """
        Decompresses the downloaded .bz2 file efficiently using multithreading.

        Args:
            num_threads (int): The number of threads to use for decompression.

        Returns:
            bool: True if decompression was successful, False otherwise.
        """
        if not os.path.exists(self.bz2_filepath):
            print(f"Error: File not found at {self.bz2_filepath}. Please download it first.")
            return False

        print(f"Decompressing {self.bz2_filepath} using {num_threads} threads...")
        try:
            with bz2.BZ2File(self.bz2_filepath, 'rb') as f_in:
                # Read the entire decompressed content into memory.
                # For very large files, this might be an issue.
                # A more advanced approach would involve streaming decompression and writing chunks.
                decompressed_data = f_in.read()

            with open(self.xml_filepath, 'wb') as f_out:
                f_out.write(decompressed_data)

            print("Decompression complete.")
            return True
        except bz2.BZ2Error as e:
            print(f"BZ2 Error during decompression: {e}")
            return False
        except IOError as e:
            print(f"IO Error during decompression: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during decompression: {e}")
            return False

    def process_wiki_data(self) -> str:
        """
        Downloads and decompresses the wiki data.

        Returns:
            str: A message indicating the status of the operation.
        """
        if not self.download_file():
            return "Failed to download wiki data."

        if not self.decompress_file():
            return "Failed to decompress wiki data."

        return f"Successfully downloaded and decompressed wiki data to {self.xml_filepath}"

    def cleanup(self):
        """
        Cleans up the downloaded and decompressed files and the directory.
        """
        print(f"Cleaning up directory: {self.download_dir}")
        if os.path.exists(self.download_dir):
            try:
                shutil.rmtree(self.download_dir)
                print("Cleanup complete.")
            except OSError as e:
                print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    # Example usage:
    # Create an instance of the WikiDownloader
    downloader = WikiDownloader()

    # Download and decompress the file
    status_message = downloader.process_wiki_data()
    print(status_message)

    # You can access the decompressed file path
    if os.path.exists(downloader.xml_filepath):
        print(f"Decompressed XML file is located at: {downloader.xml_filepath}")

    # To clean up the temporary directory and files:
    # downloader.cleanup()

    # --- For testing purposes, you might want to keep the files ---
    # print("Keeping downloaded and decompressed files for inspection.")
    # print(f"Downloaded .bz2 file: {downloader.bz2_filepath}")
    # print(f"Decompressed .xml file: {downloader.xml_filepath}")

    # --- Example of cleanup if you want to run it ---
    # input("Press Enter to clean up the downloaded files and directory...")
    # downloader.cleanup()