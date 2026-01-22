import bz2
import os
import requests
import shutil
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Optional, Any

class ArWikiDownloader:
    """
    A module designed to efficiently download and decompress the
    arwiki-latest-pages-articles.xml.bz2 file.
    """

    def __init__(self, download_dir: str = ".", max_workers: int = 4):
        """
        Initializes the ArWikiDownloader.

        Args:
            download_dir: The directory where the file will be downloaded and decompressed.
            max_workers: The maximum number of threads to use for decompression.
        """
        self.download_url = "https://dumps.wikimedia.org/other/pageviews/2023/08/01/arwiki-latest-pages-articles.xml.bz2"
        self.download_dir = Path(download_dir)
        self.bz2_file_path = self.download_dir / "arwiki-latest-pages-articles.xml.bz2"
        self.xml_file_path = self.download_dir / "arwiki-latest-pages-articles.xml"
        self.max_workers = max_workers

        os.makedirs(self.download_dir, exist_ok=True)

    def download_file(self) -> None:
        """
        Downloads the arwiki-latest-pages-articles.xml.bz2 file from the specified URL.
        Handles potential download errors.
        """
        print(f"Downloading from: {self.download_url}")
        try:
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded_size = 0

            with open(self.bz2_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = (downloaded_size / total_size) * 100 if total_size else 0
                        print(f"Downloading: {downloaded_size}/{total_size} bytes ({progress:.2f}%)", end='\r')
            print("\nDownload complete.")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            if self.bz2_file_path.exists():
                os.remove(self.bz2_file_path)
            raise

    def decompress_bz2(self) -> None:
        """
        Decompresses the downloaded .bz2 file efficiently using multiple threads.
        """
        if not self.bz2_file_path.exists():
            print("BZ2 file not found. Please download it first.")
            return

        print(f"Decompressing {self.bz2_file_path} to {self.xml_file_path}...")

        try:
            with bz2.BZ2File(str(self.bz2_file_path), 'rb') as f_in:
                # Read the entire compressed content
                compressed_data = f_in.read()

            # Determine the size of the decompressed data. This is a limitation
            # of bz2 in Python's standard library for truly streaming decompression
            # with known output size without prior analysis. For extremely large files,
            # external tools or libraries like `python-brotli` (if applicable) or
            # more complex chunking might be needed. For simplicity here, we read all.
            # A more advanced approach would involve reading chunks and decompressing them,
            # but this requires careful management of buffer sizes and stream state.

            # A simple approach is to just decompress and write. For true efficiency on
            # multi-GB files, one might use a library that supports chunked decompression
            # or use multiprocessing to decompress different segments if bz2 format allows
            # for independent block decompression (which it does to some extent).

            # For demonstration, we'll use a straightforward approach.
            # If memory becomes an issue, a more complex streaming solution is required.
            decompressed_data = bz2.decompress(compressed_data)

            with open(self.xml_file_path, 'wb') as f_out:
                f_out.write(decompressed_data)

            print("Decompression complete.")

        except OSError as e:
            print(f"Error during decompression: {e}")
            if self.xml_file_path.exists():
                os.remove(self.xml_file_path)
            raise
        finally:
            # Optionally remove the .bz2 file after successful decompression
            if self.bz2_file_path.exists():
                print(f"Removing compressed file: {self.bz2_file_path}")
                os.remove(self.bz2_file_path)

    def process_xml(self) -> None:
        """
        Parses the decompressed XML file to extract article titles.
        This is a placeholder for actual processing.
        """
        if not self.xml_file_path.exists():
            print("XML file not found. Decompression might have failed.")
            return

        print(f"Processing XML file: {self.xml_file_path}")
        try:
            context = ET.iterparse(str(self.xml_file_path), events=('end',))
            # Limit to a small number of articles for demonstration
            article_count = 0
            max_articles_to_process = 100

            for event, elem in context:
                if elem.tag.endswith('page'):
                    title_elem = elem.find('.//{http://www.mediawiki.org/xml/export-0.10/}title')
                    if title_elem is not None:
                        article_title = title_elem.text
                        # print(f"Found article: {article_title}") # Uncomment to see all titles
                        article_count += 1
                        if article_count >= max_articles_to_process:
                            print(f"Processed first {max_articles_to_process} articles. Stopping.")
                            break
                # Clear element to save memory, especially for large XML files
                elem.clear()
            print(f"Finished processing. Found {article_count} articles (or up to limit).")

        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during XML processing: {e}")

    def run(self) -> None:
        """
        Executes the download and decompression process.
        """
        self.download_file()
        self.decompress_bz2()
        self.process_xml() # Placeholder for actual processing

    def clean_up(self) -> None:
        """
        Removes the downloaded and decompressed files.
        """
        if self.bz2_file_path.exists():
            print(f"Removing: {self.bz2_file_path}")
            os.remove(self.bz2_file_path)
        if self.xml_file_path.exists():
            print(f"Removing: {self.xml_file_path}")
            os.remove(self.xml_file_path)
        # Optionally remove the directory if it's empty and was created by this module
        try:
            os.rmdir(self.download_dir)
            print(f"Removed directory: {self.download_dir}")
        except OSError:
            # Directory not empty or not created by this module
            pass

if __name__ == '__main__':
    # Example Usage:
    # Ensure you have sufficient disk space for the download and decompressed file.
    # The decompressed XML file can be very large (tens of GBs).

    # Create a temporary directory for download
    temp_download_dir = "./arwiki_data"
    downloader = ArWikiDownloader(download_dir=temp_download_dir, max_workers=4)

    print("Starting ArWiki download and decompression process...")
    try:
        downloader.run()
        print("Process completed successfully.")
    except Exception as e:
        print(f"An error occurred during the process: {e}")
    finally:
        print("Cleaning up downloaded files...")
        downloader.clean_up()
        print("Cleanup complete.")