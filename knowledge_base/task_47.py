import bz2
import requests
import os
import logging
import shutil
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DownloadError(Exception):
    """Custom exception for download errors."""
    pass

class DecompressionError(Exception):
    """Custom exception for decompression errors."""
    pass

class ArwikiDownloader:
    """
    A module to download and decompress the arwiki-latest-pages-articles.xml.bz2 file.
    """
    def __init__(self, download_dir=".", chunk_size=8192):
        """
        Initializes the ArwikiDownloader.

        Args:
            download_dir (str): The directory where the file will be downloaded.
            chunk_size (int): The size of chunks to read/write during download and decompression.
        """
        self.download_dir = os.path.abspath(download_dir)
        self.chunk_size = chunk_size
        self.download_url = "https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2"
        self.downloaded_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml.bz2")
        self.decompressed_filepath = os.path.join(self.download_dir, "arwiki-latest-pages-articles.xml")
        os.makedirs(self.download_dir, exist_ok=True)

    def _download_file(self):
        """
        Downloads the arwiki-latest-pages-articles.xml.bz2 file.
        """
        logging.info(f"Starting download from: {self.download_url}")
        try:
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(self.downloaded_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            logging.info(f"Downloading... {progress:.2f}% ({downloaded_size}/{total_size} bytes)")
                        else:
                            logging.info(f"Downloading... {downloaded_size} bytes")
            logging.info(f"Successfully downloaded to: {self.downloaded_filepath}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during download: {e}")
            if os.path.exists(self.downloaded_filepath):
                os.remove(self.downloaded_filepath)
            raise DownloadError(f"Failed to download the file: {e}")

    def _decompress_file(self):
        """
        Decompresses the downloaded .bz2 file to .xml.
        """
        if not os.path.exists(self.downloaded_filepath):
            raise DecompressionError("Downloaded file not found. Please download first.")

        logging.info(f"Starting decompression of: {self.downloaded_filepath}")
        try:
            with bz2.BZ2File(self.downloaded_filepath, 'rb') as f_in, open(self.decompressed_filepath, 'wb') as f_out:
                # Get total size for progress calculation
                input_file_size = os.path.getsize(self.downloaded_filepath)
                decompressed_size = 0

                while True:
                    chunk = f_in.read(self.chunk_size)
                    if not chunk:
                        break
                    f_out.write(chunk)
                    decompressed_size += len(chunk)
                    if input_file_size > 0:
                        progress = (decompressed_size / input_file_size) * 100
                        logging.info(f"Decompressing... {progress:.2f}%")
                    else:
                        logging.info(f"Decompressing... {decompressed_size} bytes")

            logging.info(f"Successfully decompressed to: {self.decompressed_filepath}")
        except IOError as e:
            logging.error(f"Error during decompression: {e}")
            if os.path.exists(self.decompressed_filepath):
                os.remove(self.decompressed_filepath)
            raise DecompressionError(f"Failed to decompress the file: {e}")
        finally:
            # Clean up the compressed file after successful decompression
            if os.path.exists(self.downloaded_filepath):
                try:
                    os.remove(self.downloaded_filepath)
                    logging.info(f"Removed compressed file: {self.downloaded_filepath}")
                except OSError as e:
                    logging.warning(f"Could not remove compressed file {self.downloaded_filepath}: {e}")

    def download_and_decompress(self, force_download=False):
        """
        Downloads and decompresses the arwiki-latest-pages-articles.xml.bz2 file.

        Args:
            force_download (bool): If True, re-downloads the file even if it exists.

        Returns:
            str: The path to the decompressed XML file if successful, None otherwise.
        """
        if os.path.exists(self.decompressed_filepath) and not force_download:
            logging.info(f"Decompressed file already exists: {self.decompressed_filepath}. Skipping download and decompression.")
            return self.decompressed_filepath

        try:
            self._download_file()
            self._decompress_file()
            return self.decompressed_filepath
        except (DownloadError, DecompressionError) as e:
            logging.error(f"Operation failed: {e}")
            return None

    def get_decompressed_filepath(self):
        """
        Returns the path to the decompressed XML file.
        """
        return self.decompressed_filepath

    def cleanup(self):
        """
        Removes both the downloaded and decompressed files.
        """
        logging.info("Cleaning up downloaded and decompressed files...")
        if os.path.exists(self.downloaded_filepath):
            try:
                os.remove(self.downloaded_filepath)
                logging.info(f"Removed: {self.downloaded_filepath}")
            except OSError as e:
                logging.warning(f"Could not remove {self.downloaded_filepath}: {e}")
        if os.path.exists(self.decompressed_filepath):
            try:
                os.remove(self.decompressed_filepath)
                logging.info(f"Removed: {self.decompressed_filepath}")
            except OSError as e:
                logging.warning(f"Could not remove {self.decompressed_filepath}: {e}")
        # Optionally remove the directory if it's empty
        try:
            if not os.listdir(self.download_dir):
                os.rmdir(self.download_dir)
                logging.info(f"Removed empty directory: {self.download_dir}")
        except OSError as e:
            logging.warning(f"Could not remove directory {self.download_dir}: {e}")


# Example Usage:
if __name__ == "__main__":
    # Define a directory for downloads
    DOWNLOAD_DIRECTORY = "./arwiki_data"
    downloader = ArwikiDownloader(download_dir=DOWNLOAD_DIRECTORY)

    print("--- Starting Arwiki Download and Decompression ---")

    # Ensure cleanup before starting a new run if files might exist from previous runs
    # downloader.cleanup()

    # Download and decompress
    decompressed_file = downloader.download_and_decompress()

    if decompressed_file:
        print(f"\nSuccessfully obtained decompressed file at: {decompressed_file}")
        print(f"File size: {os.path.getsize(decompressed_file)} bytes")

        # You can now process the decompressed XML file.
        # For example, you could read the first few lines:
        try:
            with open(decompressed_file, 'r', encoding='utf-8') as f:
                print("\nFirst 10 lines of the decompressed file:")
                for i in range(10):
                    line = f.readline()
                    if line:
                        print(line.strip())
                    else:
                        break
        except Exception as e:
            print(f"Error reading decompressed file: {e}")

    else:
        print("\nFailed to download and decompress the Arwiki file.")

    print("\n--- Cleaning up Arwiki data ---")
    # Clean up the downloaded and decompressed files
    downloader.cleanup()
    print("Cleanup complete.")

    print("\n--- Testing Scenario: File already exists ---")
    # Simulate downloading again when the file already exists
    # Create a dummy decompressed file
    dummy_decompressed_path = os.path.join(DOWNLOAD_DIRECTORY, "arwiki-latest-pages-articles.xml")
    os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)
    with open(dummy_decompressed_path, "w") as f:
        f.write("<dummy>content</dummy>")
    print(f"Created dummy decompressed file: {dummy_decompressed_path}")

    downloader_rerun = ArwikiDownloader(download_dir=DOWNLOAD_DIRECTORY)
    print("Attempting to download and decompress again (should skip).")
    decompressed_file_rerun = downloader_rerun.download_and_decompress()

    if decompressed_file_rerun:
        print(f"File found at: {decompressed_file_rerun} (as expected)")
    else:
        print("Error: File was not found when it should have existed.")

    print("\n--- Testing Scenario: Force Download ---")
    print("Attempting to download and decompress with force_download=True.")
    decompressed_file_forced = downloader_rerun.download_and_decompress(force_download=True)

    if decompressed_file_forced:
        print(f"File obtained after forced download: {decompressed_file_forced}")
    else:
        print("Error: Failed to obtain file during forced download.")

    print("\n--- Final Cleanup ---")
    downloader.cleanup()
    print("Final cleanup complete.")