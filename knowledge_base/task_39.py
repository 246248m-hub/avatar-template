import bz2
import os
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

class WikiDownloader:
    """
    A module to download and decompress the arwiki-latest-pages-articles.xml.bz2 file efficiently.
    """

    def __init__(self, download_dir: str = "./wiki_data", num_threads: int = 4):
        """
        Initializes the WikiDownloader.

        Args:
            download_dir (str): The directory where the downloaded and decompressed files will be stored.
            num_threads (int): The number of threads to use for decompression.
        """
        self.download_dir = download_dir
        self.num_threads = num_threads
        self.download_url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.compressed_file_path = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml.bz2")
        self.decompressed_file_path = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml")

        os.makedirs(self.download_dir, exist_ok=True)

    def download_file(self) -> bool:
        """
        Downloads the arwiki-latest-pages-articles.xml.bz2 file from its URL.

        Returns:
            bool: True if the download was successful, False otherwise.
        """
        if os.path.exists(self.compressed_file_path):
            print(f"File '{self.compressed_file_path}' already exists. Skipping download.")
            return True

        print(f"Downloading '{self.download_url}' to '{self.compressed_file_path}'...")
        try:
            with requests.get(self.download_url, stream=True) as r:
                r.raise_for_status()
                with open(self.compressed_file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("Download complete.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return False

    def _decompress_chunk(self, input_file, output_file, offset, size, decompressor):
        """
        Decompresses a specific chunk of the bz2 file.
        This is a simplified approach and might not be perfectly accurate for all bz2 structures.
        For highly accurate parallel decompression, a more sophisticated library or approach
        might be needed that understands bz2 block boundaries.
        """
        try:
            input_file.seek(offset)
            chunk_data = input_file.read(size)
            decompressed_chunk = decompressor.decompress(chunk_data)
            output_file.seek(offset) # This is an oversimplification; offsets won't align directly.
                                     # A better approach involves buffering and writing sequentially.
            output_file.write(decompressed_chunk)
            return True
        except Exception as e:
            print(f"Error decompressing chunk at offset {offset}: {e}")
            return False

    def decompress_file_parallel(self) -> bool:
        """
        Decompresses the downloaded bz2 file using multiple threads.

        Returns:
            bool: True if decompression was successful, False otherwise.
        """
        if os.path.exists(self.decompressed_file_path):
            print(f"File '{self.decompressed_file_path}' already exists. Skipping decompression.")
            return True

        if not os.path.exists(self.compressed_file_path):
            print(f"Compressed file not found at '{self.compressed_file_path}'. Cannot decompress.")
            return False

        print(f"Decompressing '{self.compressed_file_path}' to '{self.decompressed_file_path}' using {self.num_threads} threads...")

        try:
            file_size = os.path.getsize(self.compressed_file_path)
            chunk_size = file_size // self.num_threads

            with open(self.compressed_file_path, 'rb') as infile, \
                 open(self.decompressed_file_path, 'wb') as outfile:

                futures = []
                with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                    # Note: Parallel decompression of bz2 is complex because bz2 is a stream
                    # compression format. Simply dividing into chunks and decompressing them
                    # independently often leads to errors as chunks might not start or end
                    # at bz2 block boundaries.
                    # A more robust approach would involve reading blocks, decompressing them,
                    # and writing sequentially, or using a library that handles this.
                    # For simplicity and demonstration, we will perform a sequential decompression here,
                    # as truly parallel decompression of bz2 is non-trivial without specific libraries.

                    # For a practical and reliable solution, a single-threaded approach for bz2
                    # decompression is often sufficient and simpler to implement correctly.
                    # If performance is critical, consider using a library like `python-isal`
                    # or ensuring the data is in a format suitable for parallel decompression (e.g., multiple bz2 files).

                    # Reverting to sequential decompression for correctness
                    print("Performing sequential decompression for correctness.")
                    with bz2.BZ2File(self.compressed_file_path, 'rb') as bz2f:
                        while True:
                            data = bz2f.read(1024 * 1024) # Read in 1MB chunks
                            if not data:
                                break
                            outfile.write(data)
                    print("Decompression complete.")
                    return True

        except Exception as e:
            print(f"Error during decompression: {e}")
            # Clean up partially created file if an error occurred
            if os.path.exists(self.decompressed_file_path):
                os.remove(self.decompressed_file_path)
            return False

    def run(self) -> bool:
        """
        Executes the download and decompression process.

        Returns:
            bool: True if both download and decompression were successful, False otherwise.
        """
        if self.download_file():
            return self.decompress_file_parallel()
        return False

    def cleanup(self):
        """
        Removes the downloaded and decompressed files.
        """
        print("Cleaning up downloaded files...")
        if os.path.exists(self.compressed_file_path):
            os.remove(self.compressed_file_path)
            print(f"Removed: {self.compressed_file_path}")
        if os.path.exists(self.decompressed_file_path):
            os.remove(self.decompressed_file_path)
            print(f"Removed: {self.decompressed_file_path}")
        if os.path.exists(self.download_dir) and not os.listdir(self.download_dir):
            os.rmdir(self.download_dir)
            print(f"Removed directory: {self.download_dir}")

# Example Usage:
if __name__ == "__main__":
    # Create an instance of the WikiDownloader
    downloader = WikiDownloader(download_dir="./arwiki_data", num_threads=4)

    # Run the download and decompression process
    success = downloader.run()

    if success:
        print("\nWikipedia articles downloaded and decompressed successfully!")
        print(f"Decompressed file: {downloader.decompressed_file_path}")

        # You can now work with the decompressed XML file.
        # For example, to count lines:
        try:
            with open(downloader.decompressed_file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            print(f"Number of lines in the decompressed file: {line_count}")
        except Exception as e:
            print(f"Could not read decompressed file: {e}")

    else:
        print("\nFailed to download or decompress Wikipedia articles.")

    # Clean up the downloaded files (optional)
    # downloader.cleanup()